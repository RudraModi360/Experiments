"""Web search and page-fetch tools."""

from __future__ import annotations

import os
import re
import textwrap
from typing import List

import requests

from ..utilities.formatting import fmt_size
from ..utilities.html_text import HtmlTextExtractor
from ..utilities.text import clip
from .context import ToolExecutionContext
from .filesystem import FileSystemTools
from .result import ToolError, ToolResult


class WebTools:
    def __init__(self, ctx: ToolExecutionContext, filesystem: FileSystemTools):
        self.ctx = ctx
        self.filesystem = filesystem

    def web_search(self, query: str, max_results: int = 5) -> ToolResult:
        query = query.strip()
        if not query:
            raise ToolError("web_search needs a non-empty query")
        api_key = os.environ.get("EXA_API_KEY", "").strip()
        if not api_key:
            raise ToolError("EXA_API_KEY is not set; web search is unavailable")
        try:
            response = requests.post(
                "https://api.exa.ai/search",
                headers={"x-api-key": api_key, "Content-Type": "application/json"},
                json={"query": query, "type": "auto", "numResults": min(max(1, max_results), 10),
                      "contents": {"text": True}},
                timeout=self.ctx.cfg.web_timeout)
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            raise ToolError(f"web search failed: {exc}") from exc
        except ValueError as exc:
            raise ToolError(f"web search returned invalid JSON: {exc}") from exc
        items = [i for i in (payload.get("results", []) if isinstance(payload, dict) else []) if isinstance(i, dict)]
        compact, full = [], []
        for n, item in enumerate(items, 1):
            title, url = item.get("title") or "(untitled)", item.get("url") or ""
            text = (item.get("text") or item.get("snippet") or "").strip()
            date = item.get("publishedDate") or ""
            self.ctx.state.add_url(url, clip(title, 60))
            compact.append(f"{n}. {title}\n   {url}{' | ' + date[:10] if date else ''}\n   {clip(' '.join(text.split()), 450)}")
            full.append(f"{n}. {title}\n{url}\n{date}\n{text[:4000]}\n")
        if not items:
            return ToolResult(f"No results for '{query}'.")
        text = f"{len(items)} result(s) for '{query}':\n" + "\n".join(compact)
        path = self.ctx.save_spill("web_search", "\n".join(full))
        self.ctx.state.add_saved(path, f"web_search('{clip(query, 50)}') full text")
        return ToolResult(text + f"\n[full result text saved: {path}]", capped=True)

    def fetch_url(self, url: str) -> ToolResult:
        if not re.match(r"^https?://", url.strip(), re.I):
            raise ToolError("only http(s) URLs are supported")
        url = url.strip()
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (intelligent-agent)"},
                                    timeout=self.ctx.cfg.fetch_timeout, stream=True)
            response.raise_for_status()
            chunks, size = [], 0
            for chunk in response.iter_content(65536):
                chunks.append(chunk)
                size += len(chunk)
                if size >= self.ctx.cfg.fetch_max_bytes:
                    break
            response.close()
        except requests.RequestException as exc:
            raise ToolError(f"fetch failed: {exc}") from exc
        kind = (response.headers.get("content-type") or "").lower()
        raw = b"".join(chunks)
        text = raw.decode(response.encoding or "utf-8", "replace")
        title = ""
        if "html" in kind or text.lstrip()[:15].lower().startswith(("<!doctype", "<html")):
            parser = HtmlTextExtractor()
            parser.feed(text)
            title = " ".join(parser.title.split())
            lines = [re.sub(r"[ \t\r\f\v]+", " ", ln).strip() for ln in "".join(parser.parts).split("\n")]
            wrapped: List[str] = []
            for ln in lines:
                if ln:
                    wrapped.extend(textwrap.wrap(ln, 160) or [ln])
                elif wrapped and wrapped[-1]:
                    wrapped.append("")
            text = "\n".join(wrapped)
        elif not any(k in kind for k in ("text", "json", "xml", "javascript")):
            raise ToolError(f"unsupported content type '{kind or 'unknown'}' ({fmt_size(len(raw))})")
        body = f"URL: {url}\nTITLE: {title}\n\n{text}"
        path = self.ctx.save_spill("page", body)
        self.ctx.state.add_url(url, clip(title, 60))
        self.ctx.state.add_saved(path, f"fetch_url({clip(url, 70)}) page text")
        info = self.filesystem.read_core(path, 1, 150, 0, max(800, self.ctx.cap - 500))
        more = f" | read more: read_file(path, offset={info['last'] + 1})" if info["last"] < info["total"] else ""
        header = (f"[fetch_url {url} | saved to {path} | lines {info['first']}-{info['last']} of {info['total']}{more}]")
        return ToolResult(header + "\n" + info["text"], capped=True)
