#!/usr/bin/env python3
import os
import sys
import glob
import math
import re
from collections import Counter, defaultdict

class SimpleBM25Retriever:
    def __init__(self, docs_dir="docs", k1=1.5, b=0.75):
        self.docs_dir = docs_dir
        self.k1 = k1
        self.b = b
        self.chunks = [] # list of dict: {id, text, source}
        self.doc_freqs = Counter()
        self.idf = {}
        self.avgdl = 0.0
        self.doc_lens = []
        self.doc_term_freqs = []
        self.build_index()

    def tokenize(self, text):
        return re.findall(r'\b\w+\b', text.lower())

    def chunk_document(self, filepath, text):
        # Chunk by paragraph or fixed size paragraphs/lines
        # For small docs or markdown, splitting by double newline or headers / paragraphs
        lines = text.splitlines()
        current_chunk = []
        chunks = []
        
        for line in lines:
            if line.startswith('#') and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = [line]
            else:
                current_chunk.append(line)
        if current_chunk:
            chunks.append("\n".join(current_chunk))
        
        # If no chunks made or empty, fallback to whole text
        if not chunks or (len(chunks) == 1 and not chunks[0].strip()):
            chunks = [text]

        # Further subdivide very long chunks if needed, but here docs are small.
        # Let's ensure non-empty chunks
        final_chunks = []
        for c in chunks:
            c_stripped = c.strip()
            if c_stripped:
                final_chunks.append(c_stripped)
        if not final_chunks:
            final_chunks = [text]
        return final_chunks

    def build_index(self):
        pattern = os.path.join(self.docs_dir, "**", "*.md")
        filepaths = glob.glob(pattern, recursive=True)
        if not filepaths:
            # try flat
            filepaths = glob.glob(os.path.join(self.docs_dir, "*.md"))

        chunk_id = 0
        all_doc_tokens = []

        for fp in sorted(filepaths):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                continue
            
            source_name = os.path.basename(fp)
            doc_chunks = self.chunk_document(fp, content)
            for c in doc_chunks:
                tokens = self.tokenize(c)
                self.chunks.append({
                    "id": chunk_id,
                    "text": c,
                    "source": source_name,
                    "filepath": fp
                })
                self.doc_lens.append(len(tokens))
                tf = Counter(tokens)
                self.doc_term_freqs.append(tf)
                for term in tf.keys():
                    self.doc_freqs[term] += 1
                chunk_id += 1
                all_doc_tokens.append(tokens)

        num_docs = len(self.chunks)
        if num_docs > 0:
            self.avgdl = sum(self.doc_lens) / num_docs
        else:
            self.avgdl = 0.0

        # Compute IDF
        for term, freq in self.doc_freqs.items():
            # BM25 IDF variant (standard Robertson-Spärck Jones)
            # IDF = ln( (N - n(q) + 0.5) / (n(q) + 0.5) + 1 )
            idf_val = math.log(1.0 + (num_docs - freq + 0.5) / (freq + 0.5))
            self.idf[term] = max(0.0, idf_val)

    def search(self, query, top_k=3):
        query_tokens = self.tokenize(query)
        scores = [0.0] * len(self.chunks)

        for idx, tf in enumerate(self.doc_term_freqs):
            score = 0.0
            doc_len = self.doc_lens[idx]
            for term in query_tokens:
                if term not in tf:
                    continue
                freq = tf[term]
                idf = self.idf.get(term, 0.0)
                # BM25 formula
                numerator = idf * freq * (self.k1 + 1.0)
                denominator = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avgdl if self.avgdl > 0 else 1.0))
                score += numerator / denominator
            scores[idx] = score

        # Rank
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        results = []
        for i in ranked_indices[:top_k]:
            if scores[i] <= 0.0 and i > 0 and len(results) >= top_k:
                # If zero score and we already have some results, or keep top_k anyway
                pass
            results.append({
                "score": scores[i],
                "chunk": self.chunks[i]
            })
        return results[:top_k]

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 rag.py \"Your question here\"")
        sys.exit(1)

    query = sys.argv[1]
    retriever = SimpleBM25Retriever()
    results = retriever.search(query, top_k=1)

    if not results or results[0]["score"] == 0.0:
        # Fallback search if zero score, just show top result or search without strict match
        results = retriever.search(query, top_k=1)

    if results:
        top = results[0]
        chunk = top["chunk"]
        print(f"Source: {chunk['source']}")
        print(f"Score: {top['score']:.4f}")
        print("Answer Excerpt:")
        print(chunk["text"])
    else:
        print("No relevant documents found.")

if __name__ == "__main__":
    main()
