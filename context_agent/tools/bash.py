"""Bash command execution tool."""

from __future__ import annotations

import os
import re
import select
import shutil
import signal
import subprocess
import time
from typing import List, Optional

from .context import ToolExecutionContext
from .result import ToolError, ToolResult


class BashTool:
    _HOST_SCAN_RE = re.compile(
        r"(?:^|[;&|]\s*)(?:find|ls)\b[^|;&\n]*?(?:\s/(?:\s|$|[|;&])|\s/(?:System|usr|Library|Users|private|var|etc|opt|Volumes)\b)"
    )
    _EARLY_PIPE_RE = re.compile(r"\|\s*(?:head|sed\s+-n|grep\s+-[^\s]*m)\b")

    def __init__(self, ctx: ToolExecutionContext):
        self.ctx = ctx

    def run(self, command: str, cwd: str = ".", timeout: Optional[int] = None) -> ToolResult:
        command = (command or "").strip()
        if not command:
            raise ToolError("bash needs a non-empty command")
        if self._HOST_SCAN_RE.search(command):
            raise ToolError("Searching outside the workspace (e.g. 'find /' or host system directories) is not allowed; stay inside the current workspace ('.').")
        workdir = self.ctx.resolve(cwd)
        if not os.path.isdir(workdir):
            raise ToolError(f"'{self.ctx.short_path(workdir)}' is not a directory")
        seconds = self.ctx.cfg.bash_timeout if timeout is None else int(timeout)
        seconds = max(1, min(seconds, self.ctx.cfg.bash_timeout_max))
        limit = max(1024, int(self.ctx.cfg.bash_max_output_bytes))
        shell = shutil.which("bash") or os.environ.get("SHELL") or "/bin/sh"
        argv = [shell, "-o", "pipefail", "-c", command] if os.path.basename(shell) == "bash" else [shell, "-c", command]
        started = time.monotonic()
        meta = {"cwd": workdir, "timeout": seconds}
        env = os.environ.copy()
        env.setdefault("CI", "true")
        env.setdefault("npm_config_yes", "true")
        env.setdefault("DEBIAN_FRONTEND", "noninteractive")
        try:
            proc = subprocess.Popen(
                argv,
                cwd=workdir,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                start_new_session=True,
            )
        except OSError as exc:
            raise ToolError(f"could not start bash: {exc}") from exc

        def terminate() -> None:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass

        assert proc.stdout is not None
        fd = proc.stdout.fileno()
        chunks: List[bytes] = []
        total = 0
        truncated = timed_out = False
        deadline = started + seconds
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    timed_out = True
                    terminate()
                    break
                ready, _, _ = select.select([fd], [], [], min(0.05, remaining))
                if ready:
                    data = os.read(fd, 65536)
                    if not data:
                        break
                    if total + len(data) > limit:
                        chunks.append(data[:limit - total])
                        total = limit
                        truncated = True
                        terminate()
                        break
                    chunks.append(data)
                    total += len(data)
                elif proc.poll() is not None:
                    break
        finally:
            remaining = deadline - time.monotonic()
            try:
                proc.wait(timeout=max(0.0, remaining))
            except subprocess.TimeoutExpired:
                timed_out = True
                terminate()
                proc.wait()
            proc.stdout.close()

        elapsed = time.monotonic() - started
        output = b"".join(chunks).decode("utf-8", "replace").rstrip("\n")
        notes = [f"[bash output truncated at {limit} bytes]"] if truncated else []
        disp_cwd = self.ctx.short_path(workdir)
        pipe_closed = (
            not timed_out
            and not truncated
            and proc.returncode == 141
            and bool(output)
            and bool(self._EARLY_PIPE_RE.search(command))
        )
        if timed_out:
            status = f"[bash timeout after {seconds}s | {elapsed:.2f}s | cwd {disp_cwd}]"
            body = output or "(no output before timeout)"
        elif pipe_closed:
            status = f"[bash exit 0 (pipe closed early) | {elapsed:.2f}s | cwd {disp_cwd}]"
            body = output
        else:
            status = f"[bash exit {proc.returncode} | {elapsed:.2f}s | cwd {disp_cwd}]"
            body = output or "(no output)"
        text = status + "\n" + body + ("\n" + "\n".join(notes) if notes else "")
        exit_code = None if timed_out else (0 if pipe_closed else proc.returncode)
        meta.update({"exit_code": exit_code,
                     "timed_out": timed_out, "truncated": truncated, "duration": round(elapsed, 3)})
        return ToolResult(text, ok=(proc.returncode == 0 or pipe_closed) and not timed_out and not truncated, meta=meta)
