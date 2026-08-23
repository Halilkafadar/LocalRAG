# Local RAG Assistant

This is a local RAG project built for the Microsoft Foundry Local Summer School. It uses Foundry Local and SQLite. No cloud APIs, no internet connection needed.

The system reads `.txt` and `.md` files from the `docs/` folder, splits them into chunks using `chunker.py`, embeds each chunk and stores it in a SQLite database, then uses `qwen2.5-1.5b` to answer questions based on retrieved context.

## Requirements

- Python 3.11+
- [Foundry Local](https://github.com/microsoft/Foundry-Local) installed (`foundry` CLI)
- `pip install -r requirements.txt`

## Setup

```bash
pip install -r requirements.txt
```

Put your `.txt` or `.md` files inside the `docs/` folder, then run:

```bash
python main.py
```

On first run it will embed all documents and store them in SQLite. After that it drops into a Q&A loop.

## Commands

- Type any question and press Enter to get an answer
- `:re-ingest` — clears the database and re-embeds everything (use after adding new docs)
- `:quit` — exits the program

## File Structure

```
mc_rag/
├── main.py            # entry point, CLI loop
├── config.py          # chunk size, model names, top-k, etc.
├── chunker.py         # splits text files into overlapping chunks
├── database.py        # SQLite setup and CRUD
├── foundry_client.py  # wraps Foundry Local SDK
├── ingestion.py       # runs the full embed + store pipeline
├── retriever.py       # cosine similarity search over stored chunks
├── generator.py       # builds the prompt and calls the LLM
├── requirements.txt
└── docs/              # put your .txt / .md knowledge files here
```

## Configuration

All tunable values are in `config.py`:

- `CHUNK_SIZE` — characters per chunk (default: 1000)
- `OVERLAP` — overlap between adjacent chunks (default: 200)
- `TOP_K` — how many chunks to retrieve per query (default: 3)
- `EMBED_MODEL` — embedding model alias (`qwen3-embedding-0.6b`)
- `CHAT_MODEL` — chat model alias (`qwen2.5-1.5b`)

## Design Decisions

I used SQLite because it doesn't require any extra setup — it's in Python's standard library and everything stays in a single file on disk.

I didn't use LangChain to keep the codebase simple and pure Python. Writing the cosine similarity and chunking logic manually made it easier to understand and debug what's actually happening.

Embedding vectors are stored as JSON strings inside SQLite. It's not the most optimal approach for very large datasets, but it works fine for this project size and avoids adding any binary serialization dependencies.

Reference: Project inspired by the Microsoft Tech Community guide on building a local RAG application for Microsoft Summer School Project internship.