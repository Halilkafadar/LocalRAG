"""SQLite store for document chunks and their embedding vectors."""

import sqlite3
import json
from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                source    TEXT    NOT NULL,
                chunk_idx INTEGER NOT NULL,
                chunk_text TEXT   NOT NULL,
                embedding TEXT    NOT NULL
            )
            """
        )
        conn.commit()


def is_populated() -> bool:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) as cnt FROM chunks").fetchone()
        return row["cnt"] > 0


def clear_db() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM chunks")
        conn.commit()


def insert_chunk(source: str, chunk_idx: int, chunk_text: str, embedding: list[float]) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO chunks (source, chunk_idx, chunk_text, embedding) VALUES (?, ?, ?, ?)",
            (source, chunk_idx, chunk_text, json.dumps(embedding)),
        )
        conn.commit()


def fetch_all_chunks() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, source, chunk_text, embedding FROM chunks").fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "source": row["source"],
            "chunk_text": row["chunk_text"],
            "embedding": json.loads(row["embedding"]),
        })
    return result
