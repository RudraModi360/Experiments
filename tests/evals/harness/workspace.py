"""Sandbox creation, artifact materialization, setup commands and workspace diffs."""

from __future__ import annotations

import csv
import fnmatch
import hashlib
import os
import re
import shutil
import signal
import subprocess
import tarfile
import tempfile
import time
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from context_agent.utilities.html_text import HtmlTextExtractor

from .case import ARTIFACTS_DIR, ArtifactSpec, Case, SetupCommand

IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".venv", "venv", "env", ".DS_Store",
}
IGNORE_FILES = {".DS_Store"}


class WorkspaceError(Exception):
    """Raised when a sandbox cannot be prepared or a setup command fails."""


# --------------------------------------------------------------------------- paths


def _safe_target(root: Path, relative: str) -> Path:
    root = root.resolve()
    target = (root / (relative or ".")).resolve()
    if target != root and root not in target.parents:
        raise WorkspaceError(f"artifact target escapes the workspace: {relative!r}")
    return target


def _excluded(relative: str, exclude: list[str]) -> bool:
    rel = relative.replace(os.sep, "/")
    name = Path(rel).name
    return any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(name, p) for p in exclude)


def _matches(relative: str, include: list[str], exclude: list[str]) -> bool:
    rel = relative.replace(os.sep, "/")
    name = Path(rel).name
    if _excluded(rel, exclude):
        return False
    if include and not any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(name, p) for p in include):
        return False
    return True


def _mapped_name(name: str, transform: str) -> str:
    path = Path(name)
    suffix = path.suffix.lower()
    mapping = {
        "html_to_text": {".html": ".txt", ".htm": ".txt"},
        "pdf_to_text": {".pdf": ".txt"},
        "csv_to_markdown": {".csv": ".md"},
    }
    if transform in mapping and suffix in mapping[transform]:
        return str(path.with_suffix(mapping[transform][suffix]))
    return name


def _dest_for_file(destination: Path, source_name: str, transform: str) -> Path:
    if destination.exists() and destination.is_dir():
        return destination / _mapped_name(source_name, transform)
    # If an exact target keeps the source extension, apply the transform suffix.
    if transform in {"html_to_text", "pdf_to_text", "csv_to_markdown"}:
        mapped = _mapped_name(destination.name, transform)
        if mapped != destination.name:
            return destination.with_name(mapped)
    return destination


# --------------------------------------------------------------------------- transforms


def _html_to_text(path: Path) -> str:
    parser = HtmlTextExtractor()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    title = " ".join(parser.title.split())
    lines = [re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in "".join(parser.parts).split("\n")]
    body = "\n".join(line for line in lines if line)
    return (title + "\n\n" + body).strip() if title else body


def _pdf_to_text(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise WorkspaceError(
            "pdf_to_text needs `pypdf`; install it or commit a .txt version of the document"
        ) from exc
    reader = PdfReader(str(path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append(f"[page {index}]\n{text}")
    return "\n\n".join(pages)


def _csv_to_markdown(path: Path) -> str:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return "(empty CSV)"
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    header, *body = rows

    def cell(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ").strip()

    lines = ["| " + " | ".join(cell(x) for x in header) + " |",
             "| " + " | ".join("---" for _ in header) + " |"]
    lines += ["| " + " | ".join(cell(x) for x in row) + " |" for row in body]
    return "\n".join(lines)


def _transform_file(source: Path, destination: Path, transform: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if transform == "copy":
        shutil.copy2(source, destination)
    elif transform == "text":
        text = source.read_bytes().decode("utf-8", "replace")
        destination.write_text(text, encoding="utf-8")
    elif transform == "html_to_text":
        destination.write_text(_html_to_text(source), encoding="utf-8")
    elif transform == "pdf_to_text":
        destination.write_text(_pdf_to_text(source), encoding="utf-8")
    elif transform == "csv_to_markdown":
        destination.write_text(_csv_to_markdown(source), encoding="utf-8")
    else:
        raise WorkspaceError(f"unsupported file transform: {transform}")


def _safe_extract_zip(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive) as zf:
        for member in zf.infolist():
            target = (destination / member.filename).resolve()
            if root not in target.parents and target != root:
                raise WorkspaceError(f"zip member escapes target: {member.filename}")
        zf.extractall(destination)


def _safe_extract_tar(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with tarfile.open(archive) as tf:
        for member in tf.getmembers():
            target = (destination / member.name).resolve()
            if root not in target.parents and target != root:
                raise WorkspaceError(f"tar member escapes target: {member.name}")
        tf.extractall(destination)


def _unpack(archive: Path, destination: Path) -> None:
    if zipfile.is_zipfile(archive):
        _safe_extract_zip(archive, destination)
    elif tarfile.is_tarfile(archive):
        _safe_extract_tar(archive, destination)
    else:
        raise WorkspaceError(f"cannot unpack (not zip/tar): {archive}")


# --------------------------------------------------------------------------- copy / fetch


def _dir_has_files(source: Path) -> bool:
    for _, dirnames, filenames in os.walk(source):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        if any(name not in IGNORE_FILES for name in filenames):
            return True
    return False


def _copy_tree(source: Path, destination: Path, spec: ArtifactSpec) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for dirpath, dirnames, filenames in os.walk(source):
        current = Path(dirpath)
        rel_dir = current.relative_to(source)
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in IGNORE_DIRS and not _excluded(str(rel_dir / d), spec.exclude)
        )
        (destination / rel_dir).mkdir(parents=True, exist_ok=True)
        for name in sorted(filenames):
            if name in IGNORE_FILES:
                continue
            rel = rel_dir / name
            if not _matches(str(rel), spec.include, spec.exclude):
                continue
            target_rel = Path(_mapped_name(str(rel), spec.transform))
            _transform_file(current / name, destination / target_rel, spec.transform)


def _symlink_tree(source: Path, destination: Path, spec: ArtifactSpec) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        # The target is an existing directory (often the workspace root).
        # Link the tree's children into it instead of replacing the root.
        if not destination.is_dir():
            raise WorkspaceError(f"symlink target is not a directory: {destination}")
        for child in sorted(source.iterdir()):
            target = destination / child.name
            if target.exists():
                raise WorkspaceError(f"symlink target already exists: {target}")
            os.symlink(child, target, target_is_directory=child.is_dir())
        return
    os.symlink(source, destination, target_is_directory=source.is_dir())


def _fetch_url(url: str, destination: Path, timeout: int = 30) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme == "file":
        source = Path(urllib.request.url2pathname(parsed.path))
        if not source.is_file():
            raise WorkspaceError(f"file URL is not a file: {source}")
        shutil.copy2(source, destination)
        return destination
    request = urllib.request.Request(url, headers={"User-Agent": "agent-eval/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
    destination.write_bytes(data)
    return destination


# --------------------------------------------------------------------------- commands


def _shell() -> str:
    return shutil.which("bash") or os.environ.get("SHELL") or "/bin/sh"


def _subprocess_env() -> dict[str, str]:
    """Environment for commands run inside a case workspace.

    DeepEval installs a global ``pytest11`` entry point. A bare ``pytest`` in a
    sandbox then crashes in the plugin's ``pytest_sessionstart`` because it
    expects ``deepeval test run`` options. Disable only that plugin; the outer
    eval run keeps using it.
    """
    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    env["AGENT_EVAL"] = "1"
    addopts = env.get("PYTEST_ADDOPTS", "")
    if "no:deepeval" not in addopts:
        env["PYTEST_ADDOPTS"] = (addopts + " -p no:deepeval").strip()
    return env


def run_command(command: str, cwd: Path, timeout: float = 60.0) -> dict[str, Any]:
    """Run a shell command and return a structured, report-friendly result."""
    env = _subprocess_env()
    started = time.monotonic()
    try:
        process = subprocess.Popen(
            [_shell(), "-c", command],
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            env=env,
            start_new_session=True,
        )
    except OSError as exc:
        return {
            "command": command,
            "cwd": str(cwd),
            "exit_code": None,
            "stdout": "",
            "stderr": str(exc),
            "timed_out": False,
            "duration": time.monotonic() - started,
        }

    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            if hasattr(os, "killpg"):
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            else:  # pragma: no cover - non-POSIX fallback
                process.kill()
        except Exception:
            process.kill()
        stdout, stderr = process.communicate()

    return {
        "command": command,
        "cwd": str(cwd),
        "exit_code": process.returncode,
        "stdout": stdout or "",
        "stderr": stderr or "",
        "timed_out": timed_out,
        "duration": time.monotonic() - started,
    }


# --------------------------------------------------------------------------- snapshots


def snapshot_manifest(root: Path) -> dict[str, dict[str, Any]]:
    """Hash every regular file under root, skipping VCS/cache directories."""
    manifest: dict[str, dict[str, Any]] = {}
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_DIRS)
        for name in sorted(filenames):
            if name in IGNORE_FILES:
                continue
            path = Path(dirpath) / name
            rel = str(path.relative_to(root)).replace(os.sep, "/")
            try:
                if path.is_symlink():
                    manifest[rel] = {"sha256": None, "size": 0, "symlink": os.readlink(path)}
                    continue
                digest = hashlib.sha256()
                size = 0
                with path.open("rb") as handle:
                    while True:
                        chunk = handle.read(1024 * 1024)
                        if not chunk:
                            break
                        size += len(chunk)
                        digest.update(chunk)
                manifest[rel] = {"sha256": digest.hexdigest(), "size": size}
            except OSError as exc:
                manifest[rel] = {"sha256": None, "size": 0, "error": str(exc)}
    return manifest


def diff_manifests(before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    before_keys, after_keys = set(before), set(after)
    modified = sorted(
        key for key in before_keys & after_keys
        if before[key].get("sha256") != after[key].get("sha256")
        or before[key].get("symlink") != after[key].get("symlink")
    )
    return {
        "added": sorted(after_keys - before_keys),
        "modified": modified,
        "deleted": sorted(before_keys - after_keys),
    }


def diff_summary(diff: dict[str, list[str]], limit: int = 40) -> str:
    lines = []
    for key in ("added", "modified", "deleted"):
        values = diff.get(key) or []
        if values:
            shown = ", ".join(values[:limit])
            suffix = f" (+{len(values) - limit} more)" if len(values) > limit else ""
            lines.append(f"{key}: {shown}{suffix}")
    return "\n".join(lines) if lines else "(no workspace changes)"


# --------------------------------------------------------------------------- workspace


@dataclass
class Workspace:
    case: Case
    base: Path
    root: Path
    agent_home: Path
    setup_results: list[dict[str, Any]] = field(default_factory=list)
    before: dict[str, dict[str, Any]] = field(default_factory=dict)
    keep: bool = False
    keep_dir: Path | None = None

    def __enter__(self) -> "Workspace":
        self.root.mkdir(parents=True, exist_ok=True)
        self.agent_home.mkdir(parents=True, exist_ok=True)
        try:
            if self.case.workspace.root:
                source = (self.case.dir / self.case.workspace.root).resolve()
                if not source.exists():
                    raise WorkspaceError(f"workspace.root does not exist: {source}")
                spec = ArtifactSpec(kind="repo", transform="copy")
                if source.is_dir():
                    _copy_tree(source, self.root, spec)
                else:
                    _transform_file(source, self.root / source.name, "copy")
            for spec in self.case.workspace.artifacts:
                self._materialize(spec)
            self._run_setup()
            self.before = snapshot_manifest(self.root)
        except Exception:
            self.cleanup()
            raise
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if self.keep and self.keep_dir is not None:
                self.keep_dir.parent.mkdir(parents=True, exist_ok=True)
                if self.keep_dir.exists():
                    shutil.rmtree(self.keep_dir)
                shutil.copytree(self.root, self.keep_dir, symlinks=True)
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        shutil.rmtree(self.base, ignore_errors=True)

    # ------------------------------------------------------------------ materialize

    def _materialize(self, spec: ArtifactSpec) -> None:
        destination = _safe_target(self.root, spec.target)
        if spec.kind == "inline":
            if spec.content is None:
                raise WorkspaceError("inline artifact has no content")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(str(spec.content), encoding="utf-8")
            return

        if spec.kind == "url":
            if not (spec.network or self.case.workspace.network):
                raise WorkspaceError("url artifact needs network = true")
            if not spec.source:
                raise WorkspaceError("url artifact needs source")
            name = Path(urllib.parse.urlparse(spec.source).path).name or "download"
            target = _dest_for_file(destination, name, spec.transform)
            temp = self.base / "download.tmp"
            try:
                _fetch_url(str(spec.source), temp)
            except Exception as exc:  # network is inherently flaky; honour optional
                if spec.optional:
                    return
                raise WorkspaceError(f"cannot fetch {spec.source}: {exc}") from exc
            if spec.transform == "copy":
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(temp, target)
            else:
                _transform_file(temp, target, spec.transform)
            return

        source: Path
        if spec.bundle:
            source = (ARTIFACTS_DIR / spec.bundle).resolve()
        elif spec.source:
            source = (self.case.dir / spec.source).resolve()
        else:
            raise WorkspaceError("artifact needs source or bundle")

        if not source.exists():
            if spec.optional:
                return
            raise WorkspaceError(f"artifact source does not exist: {source}")

        if spec.transform == "unpack":
            _unpack(source, destination)
            return

        if spec.kind in {"repo", "docs"}:
            if not source.is_dir():
                raise WorkspaceError(f"{spec.kind} artifact source is not a directory: {source}")
            if not spec.optional and "greenfield" not in self.case.tags and not _dir_has_files(source):
                raise WorkspaceError(f"{spec.kind} artifact directory is empty (0 files): {source}")
            if spec.mode == "symlink":
                _symlink_tree(source, destination, spec)
            else:
                _copy_tree(source, destination, spec)
            return

        if not source.is_file():
            raise WorkspaceError(f"file artifact source is not a file: {source}")
        target = _dest_for_file(destination, source.name, spec.transform)
        if spec.mode == "symlink":
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                raise WorkspaceError(f"symlink target already exists: {target}")
            os.symlink(source, target)
        else:
            _transform_file(source, target, spec.transform)

    # ------------------------------------------------------------------ setup

    def _run_setup(self) -> None:
        for setup in self.case.workspace.setup:
            cwd = _safe_target(self.root, setup.cwd)
            if not cwd.is_dir():
                raise WorkspaceError(f"setup cwd is not a directory: {cwd}")
            result = run_command(setup.command, cwd, setup.timeout)
            self.setup_results.append(result)
            if result["timed_out"] or result["exit_code"] != 0:
                if setup.optional:
                    continue
                detail = (result.get("stderr") or result.get("stdout") or "").strip()
                raise WorkspaceError(
                    f"setup command failed ({result['exit_code']}): {setup.command}\n{detail[-2000:]}"
                )


def create_workspace(case: Case) -> Workspace:
    base = Path(tempfile.mkdtemp(prefix=f"agenteval-{case.id}-"))
    return Workspace(
        case=case,
        base=base,
        root=base / "workspace",
        agent_home=base / "agent_home",
    )
