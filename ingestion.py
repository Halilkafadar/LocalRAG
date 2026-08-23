"""Ingests documents: chunks them, embeds each chunk, and stores in SQLite."""

from chunker import load_documents, chunk_documents
from database import init_db, is_populated, clear_db, insert_chunk
from foundry_client import get_embedding_client, embed_text


def run_ingestion(force: bool = False) -> int:
    init_db()

    if is_populated() and not force:
        print("Database already populated. Use force=True to re-ingest.")
        return 0

    if force:
        clear_db()

    docs = load_documents()
    if not docs:
        print("No .txt or .md files found in docs/. Add documents and re-run.")
        return 0

    chunks = chunk_documents(docs)
    print(f"Loaded {len(docs)} document(s), produced {len(chunks)} chunk(s).")

    embed_client = get_embedding_client()
    inserted = 0
    for i, chunk in enumerate(chunks):
        vec = embed_text(chunk["chunk_text"], embed_client)
        insert_chunk(
            source=chunk["source"],
            chunk_idx=chunk["chunk_index"],
            chunk_text=chunk["chunk_text"],
            embedding=vec,
        )
        inserted += 1
        if (i + 1) % 10 == 0 or (i + 1) == len(chunks):
            print(f"  Embedded {i + 1}/{len(chunks)} chunks...")

    print(f"Ingestion complete. {inserted} chunks stored in database.")
    return inserted
