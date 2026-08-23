"""Handles model loading and embedding/chat client creation via Foundry Local SDK."""

from foundry_local_sdk import FoundryLocalManager, Configuration
from config import EMBED_MODEL, CHAT_MODEL

_manager: FoundryLocalManager | None = None


def _get_manager() -> FoundryLocalManager:
    global _manager
    if _manager is None:
        cfg = Configuration(app_name="local-rag")
        FoundryLocalManager.initialize(cfg)
        _manager = FoundryLocalManager.instance
    return _manager


def get_embedding_client():
    mgr = _get_manager()
    model = mgr.catalog.get_model(EMBED_MODEL)
    if model is None:
        raise RuntimeError(f"Embedding model '{EMBED_MODEL}' not found in catalog.")
    if not model.is_cached:
        print(f"Downloading {EMBED_MODEL}...")
        model.download()
    model.load()
    return model.get_embedding_client()


def get_chat_client():
    mgr = _get_manager()
    model = mgr.catalog.get_model(CHAT_MODEL)
    if model is None:
        raise RuntimeError(f"Chat model '{CHAT_MODEL}' not found in catalog.")
    if not model.is_cached:
        print(f"Downloading {CHAT_MODEL}...")
        model.download()
    model.load()
    return model.get_chat_client()


def embed_text(text: str, client=None) -> list[float]:
    if client is None:
        client = get_embedding_client()
    response = client.generate_embedding(text)
    return list(response.data[0].embedding)
