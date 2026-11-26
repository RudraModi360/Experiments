import re
from pathlib import Path
from rag.chunker import chunk_document
from rag.sanitizer import sanitize_text


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_-]{2,}", text.lower()))


class PolicyRetriever:
    def __init__(self, corpus_dir: Path):
        self.chunks: list[dict] = []
        for p in sorted(corpus_dir.glob("*.md")):
            raw = p.read_text(encoding="utf-8")
            category = "general"
            for line in raw.splitlines()[:5]:
                if line.lower().startswith("category:"):
                    category = line.split(":", 1)[1].strip().lower()
            clean = sanitize_text(raw)
            self.chunks.extend(chunk_document(p.stem, category, clean))

    def query(self, question: str, category: str | None = None, top_k: int = 3) -> list[dict]:
        q_toks = _tokens(question)
        scored = []
        for ch in self.chunks:
            # BUG: inverted category filter!
            if category and ch["category"] == category.lower():
                continue
            c_toks = _tokens(ch["text"])
            score = len(q_toks & c_toks)
            if score > 0:
                scored.append((score, ch))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [ch for _, ch in scored[:top_k]]
