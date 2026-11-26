#!/usr/bin/env python3
import sys
import os
import math
import re
from collections import Counter, defaultdict

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

class SimpleBM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = 0
        self.avgdl = 0
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.docs = []

    def fit(self, docs):
        """
        docs: list of dicts: {'id': ..., 'text': ..., 'source': ...}
        """
        self.docs = docs
        self.corpus_size = len(docs)
        if self.corpus_size == 0:
            return
        
        tokenized_docs = []
        total_len = 0
        for doc in docs:
            tokens = tokenize(doc['text'])
            tokenized_docs.append(tokens)
            dl = len(tokens)
            self.doc_len.append(dl)
            total_len += dl
            
        self.avgdl = total_len / self.corpus_size if self.corpus_size > 0 else 0

        # Document frequencies
        df = defaultdict(int)
        for tokens in tokenized_docs:
            for term in set(tokens):
                df[term] += 1

        # IDF calculation with BM25 formula (IDF smoothing)
        self.idf = {}
        for term, freq in df.items():
            self.idf[term] = math.log(1 + (self.corpus_size - freq + 0.5) / (freq + 0.5))

        # Store term frequencies per doc
        self.doc_freqs = []
        for tokens in tokenized_docs:
            self.doc_freqs.append(Counter(tokens))

    def search(self, query, top_k=3):
        query_tokens = tokenize(query)
        scores = [0.0] * self.corpus_size

        for i, doc_freq in enumerate(self.doc_freqs):
            score = 0.0
            dl = self.doc_len[i]
            for term in query_tokens:
                if term not in doc_freq:
                    continue
                tf = doc_freq[term]
                idf = self.idf.get(term, 0.0)
                # BM25 formula numerator & denominator
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (dl / self.avgdl if self.avgdl > 0 else 1))
                score += idf * (numerator / denominator)
            scores[i] = score

        # Sort by score descending
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in ranked[:top_k]:
            if score > 0:
                doc = self.docs[idx]
                results.append({
                    'score': score,
                    'text': doc['text'],
                    'source': doc['source']
                })
        return results

def load_docs(docs_dir="docs"):
    docs = []
    if not os.path.exists(docs_dir):
        return docs
    for filename in sorted(os.listdir(docs_dir)):
        if filename.endswith(".md"):
            path = os.path.join(docs_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Chunking: split by paragraphs or double newlines, or sentence/line
            # For simplicity and robustness with small markdown files, chunk by paragraphs or sections
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            if not paragraphs:
                paragraphs = [content.strip()]
            for p_idx, para in enumerate(paragraphs):
                docs.append({
                    'id': f"{filename}#chunk{p_idx}",
                    'text': para,
                    'source': filename
                })
    return docs

def get_retriever(docs_dir="docs"):
    docs = load_docs(docs_dir)
    bm25 = SimpleBM25()
    bm25.fit(docs)
    return bm25

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 rag.py \"question\"")
        sys.exit(1)
    
    query = sys.argv[1]
    bm25 = get_retriever("docs")
    results = bm25.search(query, top_k=1)
    
    if not results:
        print("No relevant answer found.")
        sys.exit(0)
        
    res = results[0]
    print(f"Source: {res['source']}")
    print(f"Answer excerpt:\n{res['text']}")

if __name__ == "__main__":
    main()
