"""Builds the augmented prompt and calls the local LLM to generate an answer."""

from retriever import retrieve
from foundry_client import get_chat_client
from config import SYSTEM_PROMPT, TOP_K


def build_context_block(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, start=1):
        parts.append(f"[Source {i}: {chunk['source']}]\n{chunk['chunk_text']}")
    return "\n\n---\n\n".join(parts)


def answer(question: str, top_k: int = TOP_K) -> dict:
    chunks = retrieve(question, top_k=top_k)

    if not chunks or chunks[0]["score"] < 0.01:
        return {
            "answer": "I don't have that information in the provided documents.",
            "sources": [],
        }

    context = build_context_block(chunks)
    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    chat_client = get_chat_client()
    completion = chat_client.complete_chat(messages)
    reply = completion.choices[0].message.content.strip()

    sources = list({c["source"] for c in chunks})
    return {"answer": reply, "sources": sources}
