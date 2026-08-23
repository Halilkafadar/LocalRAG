"""Reads text files from a directory and splits them into overlapping chunks."""

import os
from config import CHUNK_SIZE, OVERLAP, DOCS_DIR


def load_documents(directory: str = DOCS_DIR) -> list[dict]:
    docs = []
    if not os.path.isdir(directory):
        return docs
    for fname in os.listdir(directory):
        if not (fname.endswith(".txt") or fname.endswith(".md")):
            continue
        fpath = os.path.join(directory, fname)
        with open(fpath, encoding="utf-8") as f:
            text = f.read()
        docs.append({"source": fname, "text": text})
    return docs


def sliding_window_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        if end == length:
            break
        start += chunk_size - overlap
    return chunks


def chunk_documents(docs: list[dict]) -> list[dict]:
    result = []
    for doc in docs:
        raw_chunks = sliding_window_chunks(doc["text"])
        for i, chunk in enumerate(raw_chunks):
            result.append({
                "source": doc["source"],
                "chunk_index": i,
                "chunk_text": chunk.strip(),
            })
    return [c for c in result if c["chunk_text"]]
