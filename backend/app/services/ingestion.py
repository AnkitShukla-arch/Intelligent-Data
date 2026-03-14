"""Ingestion service: parses uploaded files and stores chunks in the vector DB."""
import os, shutil
from pathlib import Path
from typing import Tuple
from app.core.config import settings
from app.services import vector_store as vs

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


def save_file(file_content: bytes, filename: str) -> str:
    dest = Path(settings.UPLOAD_DIR) / filename
    with open(dest, "wb") as f:
        f.write(file_content)
    return str(dest)


def _extract_text(file_path: str, filename: str) -> str:
    """Extract plain text from PDF or text files."""
    try:
        if filename.lower().endswith(".pdf"):
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    except Exception as e:
        print(f"[Ingestion] Could not extract text: {e}")
        return ""


def _chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return [c for c in chunks if c.strip()]


def ingest_document(file_path: str, filename: str, doc_id: int, title: str, author_id: int):
    """Extract text → chunk → embed → store in ChromaDB."""
    text = _extract_text(file_path, filename)
    if not text.strip():
        return 0
    chunks = _chunk_text(text)
    metadatas = [
        {"source": title, "doc_id": doc_id, "author_id": author_id, "chunk": i}
        for i, _ in enumerate(chunks)
    ]
    vs.add_texts(chunks, metadatas)
    return len(chunks)
