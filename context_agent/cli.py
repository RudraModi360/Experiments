"""Command-line entry point for the modular Intelligent Agent."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Tuple

if __package__ in (None, ""):  # allow: python3 context_agent/cli.py
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from context_agent.cli import main as _main
    _main()
    raise SystemExit

from .agent import IntelligentAgent
from .config import Config
from .llm.errors import LLMError
from .llm.streaming import LiveTokenMeter, StreamPrinter
from .utilities.formatting import dim, format_stats, format_tool_stats, hint

HELP = """Commands
  /help                 show this help
  /model [NAME]         show the model, or switch to NAME
  /provider [NAME]      show the provider, or switch (mirai/uzu, ollama, llama-cpp, google)
  /sessions             list previous sessions grouped by day
  /resume <id|#>        resume a previous session (see /sessions)
  /new                  start a fresh session (/clear, /reset)
  /compact              force context compaction now
  /context              show token usage and context breakdown
  /state                show working memory and ledger
  /stats                show the last turn's telemetry
  /quit                 exit (/exit)
"""


def _make_printer(agent: IntelligentAgent, no_stream: bool):
    """Create a stream printer wired to the live telemetry line (TTY only)."""
    if no_stream:
        return None, None
    meter = LiveTokenMeter()
    return StreamPrinter(meter=meter), meter


def _ask(agent: IntelligentAgent, text: str, printer: StreamPrinter | None,
         meter: LiveTokenMeter | None) -> str:
    if meter:
        meter.begin()
    answer = agent.process_query(
        text,
        on_token=printer.feed if printer else None,
        on_reply=meter.reset if meter else None,
        on_stats=meter.on_stats if meter else None,
    )
    if printer:
        printer.finish()
    if meter:
        meter.finish()
    return answer


def _show_stats(agent: IntelligentAgent) -> None:
    """Print token counts and generation speed when the backend reports them."""
    line = format_stats(agent.last_stats)
    if line:
        print(hint(line))


def _show_tools(agent: IntelligentAgent) -> None:
    """Print the per-turn tool summary (calls / ok / failed / blocked)."""
    line = format_tool_stats(agent.tool_stats)
    if line:
        print(line)


def _show(agent: IntelligentAgent, answer: str, printer: StreamPrinter | None) -> None:
    """Print a reply without duplicating text that was already streamed."""
    streamed = bool(agent.last_streamed and printer and printer.visible)
    if streamed:
        if not (printer.text.endswith("\n") if printer else False):
            print()
        _show_tools(agent)
        _show_stats(agent)
        print()
        return
    if printer and printer.visible:
        print()
    print("\n" + "=" * 60 + "\n" + answer + "\n" + "=" * 60)
    _show_tools(agent)
    _show_stats(agent)


def _day_label(day: date) -> str:
    today = date.today()
    if day == today:
        return "Today"
    if day == today - timedelta(days=1):
        return "Yesterday"
    return day.strftime("%A, %d %b %Y")


def _print_sessions(sessions: List[Dict[str, Any]]) -> None:
    if not sessions:
        print("No saved sessions yet.")
        return
    print("Previous sessions:")
    day = None
    for index, item in enumerate(sessions, 1):
        label = _day_label(item["started"].date())
        if label != day:
            day = label
            print(f"\n  {hint(label)}")
        when = item["started"].strftime("%H:%M:%S")
        preview = item["preview"] or "(empty)"
        model = f" [{item['model']}]" if item.get("model") else ""
        print(f"  {index:2d}. {when}  {item['sid'][-4:]}{dim(model)}  "
              f"{item['messages']:3d} msg  {preview}")
    print("\nResume with  /resume <number>  or  /resume <session-id>")


def _setup_readline() -> None:
    """Enable Tab completion for slash commands (a lightweight palette)."""
    try:
        import readline
    except ImportError:
        return
    commands = ["/help", "/model", "/provider", "/sessions", "/resume", "/new",
                "/compact", "/context", "/state", "/stats", "/quit"]

    def completer(text: str, state: int) -> Optional[str]:
        if not text.startswith("/"):
            return None
        matches = [cmd for cmd in commands if cmd.startswith(text)]
        return matches[state] if state < len(matches) else None

    readline.set_completer(completer)
    try:
        if "libedit" in (getattr(readline, "__doc__", "") or ""):
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
    except Exception:
        pass


def _find_session(sessions: List[Dict[str, Any]], wanted: str) -> Optional[str]:
    wanted = wanted.strip()
    if not wanted:
        return None
    if wanted.isdigit():
        index = int(wanted)
        if 1 <= index <= len(sessions):
            return sessions[index - 1]["sid"]
        return None
    for item in sessions:
        if item["sid"] == wanted:
            return item["sid"]
    matches = [item["sid"] for item in sessions if item["sid"].endswith(wanted)
               or item["sid"].endswith("-" + wanted)]
    return matches[0] if len(matches) == 1 else None


def _handle_command(agent: IntelligentAgent, text: str,
                    sessions: List[Dict[str, Any]]) -> Tuple[bool, bool]:
    """Handle CLI-level slash commands.

    Returns ``(handled, should_exit)``.  Context commands (/new, /compact,
    /state, /context) fall through to the agent.
    """
    cmd, _, arg = text.partition(" ")
    cmd = cmd.lower()
    arg = arg.strip()

    if cmd in ("/quit", "/exit"):
        return True, True
    if cmd == "/help":
        print(HELP)
        return True, False
    if cmd == "/model":
        if not arg:
            print(f"model={agent.cfg.model}  (use /model NAME to switch)")
            return True, False
        try:
            print(agent.switch_model(arg))
        except LLMError as exc:
            print(f"Could not switch model: {exc}")
        return True, False
    if cmd == "/provider":
        if not arg:
            print(f"provider={agent.cfg.provider}  (use /provider NAME to switch)")
            return True, False
        try:
            print(agent.switch_provider(arg))
        except LLMError as exc:
            print(f"Could not switch provider: {exc}")
        return True, False
    if cmd in ("/sessions", "/ls"):
        sessions[:] = agent.store.list_sessions()
        _print_sessions(sessions)
        return True, False
    if cmd in ("/resume", "/open"):
        if not arg:
            print("Usage: /resume <number|session-id>   (list them with /sessions)")
            return True, False
        if not sessions:
            sessions[:] = agent.store.list_sessions()
        sid = _find_session(sessions, arg)
        if not sid:
            print(f"No unique session matches '{arg}'. Run /sessions first.")
            return True, False
        print(agent.resume_session(sid))
        return True, False
    if cmd == "/stats":
        _show_tools(agent)
        line = format_stats(agent.last_stats)
        print(line or "No telemetry yet this session.")
        return True, False
    return False, False


def _banner(cfg: Config, agent: IntelligentAgent) -> None:
    provider_detail = f" provider={cfg.provider}"
    if cfg.provider == "llama-cpp":
        provider_detail += f" endpoint={cfg.base_url or 'http://127.0.0.1:8080/v1'}"
    elif cfg.provider == "google":
        provider_detail += f" endpoint={cfg.base_url or 'Google AI Studio'}"
    print("Intelligent Agent v2 - type /help for commands, /quit to exit.")
    print(f"model={cfg.model} num_ctx={cfg.num_ctx} num_predict={cfg.num_predict}"
          f"{provider_detail} session={agent.store.sid}")
    print("-" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Intelligent Agent v2")
    parser.add_argument("--resume", nargs="?", const="", default=None, metavar="SESSION_ID",
                        help="resume the latest (or a given) session")
    parser.add_argument("--model", help="override the model name")
    parser.add_argument("--num-ctx", type=int, help="override the model context window")
    parser.add_argument("--num-predict", type=int, help="override the reply token budget")
    parser.add_argument("--provider",
                        choices=["mirai", "uzu", "ollama", "llama-cpp", "google", "gemini"],
                        help="LLM provider")
    parser.add_argument("--endpoint", help="llama.cpp or OpenAI-compatible base URL")
    parser.add_argument("--api-key", help="API key for llama.cpp or Google AI Studio")
    parser.add_argument("--quiet", action="store_true",
                        help="hide [ctx:...] trace lines (tool calls and context passes stay visible)")
    parser.add_argument("--no-tools", action="store_true", help="hide tool calls and result previews")
    parser.add_argument("--no-context", action="store_true", help="hide [ctx] compression/masking passes")
    parser.add_argument("--no-stream", action="store_true", help="wait for the full reply before printing it")
    parser.add_argument("--query", metavar="TEXT", help="run one query and exit (useful for quick tests)")
    args = parser.parse_args()

    cfg = Config()
    if args.model:
        cfg.model = args.model
    if args.num_ctx:
        cfg.num_ctx = args.num_ctx
    if args.num_predict:
        cfg.num_predict = args.num_predict
    if args.provider:
        cfg.provider = args.provider
    if args.endpoint:
        cfg.base_url = args.endpoint
    if args.api_key:
        cfg.api_key = args.api_key
    cfg.verbose = not args.quiet
    cfg.show_tools = not args.no_tools
    cfg.show_context = not args.no_context

    try:
        agent = IntelligentAgent(cfg, resume=args.resume)
    except LLMError as exc:
        print(f"Startup error: {exc}")
        sys.exit(1)

    _banner(cfg, agent)
    _setup_readline()

    if args.query is not None:
        printer, meter = _make_printer(agent, args.no_stream)
        answer = _ask(agent, args.query, printer, meter)
        _show(agent, answer, printer)
        return

    sessions: List[Dict[str, Any]] = []
    while True:
        try:
            text = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        if text.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not text:
            continue
        if text == "/":
            print(HELP)
            continue
        handled, should_exit = _handle_command(agent, text, sessions)
        if should_exit:
            print("Goodbye!")
            break
        if handled:
            continue
        printer, meter = _make_printer(agent, args.no_stream)
        answer = _ask(agent, text, printer, meter)
        _show(agent, answer, printer)


if __name__ == "__main__":
    main()
