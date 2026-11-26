def chunk_document(doc_id: str, category: str, text: str) -> list[dict]:
    # BUG: blindly slices every 90 chars, splitting clause IDs and losing section headers
    chunks = []
    for i in range(0, len(text), 90):
        chunks.append({
            "doc_id": doc_id,
            "category": category,
            "text": text[i : i + 90],
        })
    return chunks
