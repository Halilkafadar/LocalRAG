"""Entry point for the local RAG Q&A assistant."""

import sys
from ingestion import run_ingestion
from generator import answer
from database import is_populated, init_db


BANNER = """
--------------------------------------------
    Local RAG Assistant  (offline)     
    Model: qwen2.5-1.5b  |  DB: SQLite     
--------------------------------------------
Type your question and press Enter.
Commands:  :re-ingest   :quit
"""


def print_result(result: dict) -> None:
    print("\n" + "─" * 60)
    print(result["answer"])
    if result["sources"]:
        print("\nSources: " + ", ".join(result["sources"]))
    print("─" * 60 + "\n")


def main() -> None:
    print(BANNER)

    init_db()

    if not is_populated():
        print("No data found. Running ingestion first...\n")
        count = run_ingestion()
        if count == 0:
            print(
                "Ingestion produced no chunks. "
                "Place .txt or .md files inside the 'docs/' folder and restart."
            )
            sys.exit(1)

    while True:
        try:
            raw = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not raw:
            continue

        if raw == ":quit":
            print("Bye.")
            break

        if raw == ":re-ingest":
            run_ingestion(force=True)
            continue

        result = answer(raw)
        print_result(result)


if __name__ == "__main__":
    main()
