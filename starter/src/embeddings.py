"""Local Sentence Transformers embedder (real model, no API key, cost 0)."""
from __future__ import annotations

from typing import Protocol


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    def embed_query(self, question: str) -> list[float]: ...


class SentenceTransformerEmbedder:
    """all-MiniLM-L6-v2: symmetric model, so queries and documents are encoded the
    same way (no instruction prefix). Vectors are L2-normalized for cosine."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 batch_size: int = 64) -> None:
        from sentence_transformers import SentenceTransformer  # fail loudly if missing

        self.model_name = model_name
        self.batch_size = batch_size
        self.model = SentenceTransformer(model_name, device="cpu")
        self.dimensions = int(self.model.get_sentence_embedding_dimension())
        self.max_seq_length = int(self.model.max_seq_length)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vecs = self.model.encode(texts, batch_size=self.batch_size,
                                 normalize_embeddings=True, show_progress_bar=False)
        return vecs.tolist()

    def embed_query(self, question: str) -> list[float]:
        return self.model.encode([question], normalize_embeddings=True)[0].tolist()
