"""Retrieves the top-K most relevant chunks from SQLite using cosine similarity."""

import math
from database import fetch_all_chunks
from foundry_client import embed_text
from config import TOP_K


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    query_vec = embed_text(query)
    all_chunks = fetch_all_chunks()

    scored = []
    for chunk in all_chunks:
        score = cosine_similarity(query_vec, chunk["embedding"])
        scored.append({
            "source": chunk["source"],
            "chunk_text": chunk["chunk_text"],
            "score": score,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
