"""Vector store service using ChromaDB + OpenAI Embeddings."""
import os
from typing import List
from app.core.config import settings

os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings

    _client = chromadb.PersistentClient(
        path=settings.CHROMA_DB_DIR,
        settings=ChromaSettings(anonymized_telemetry=False)
    )

    def _get_embeddings():
        return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY or "sk-dummy")

    def get_vector_store() -> Chroma:
        return Chroma(
            client=_client,
            collection_name="corporate_docs",
            embedding_function=_get_embeddings()
        )

    def add_texts(texts: List[str], metadatas: List[dict]):
        store = get_vector_store()
        store.add_texts(texts=texts, metadatas=metadatas)

    def similarity_search(query: str, k: int = 4):
        store = get_vector_store()
        return store.similarity_search(query, k=k)

    VECTOR_STORE_AVAILABLE = True

except Exception as e:
    print(f"[VectorStore] Warning: ChromaDB/OpenAI not fully configured: {e}")

    def add_texts(texts, metadatas):
        pass

    def similarity_search(query, k=4):
        return []

    VECTOR_STORE_AVAILABLE = False
