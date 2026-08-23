"""Central configuration for the local RAG system."""

DB_PATH = "local_rag.db"
DOCS_DIR = "docs"

EMBED_MODEL = "qwen3-embedding-0.6b"
CHAT_MODEL = "qwen2.5-1.5b"

CHUNK_SIZE = 1000
OVERLAP = 200
TOP_K = 3

SYSTEM_PROMPT = (
    "You are a precise Q&A assistant. "
    "Answer the user's question using ONLY the context passages provided below. "
    "If the answer is not contained in the context, respond with: "
    "'I don't have that information in the provided documents.' "
    "Do not use any outside knowledge. Be concise and factual."
)
