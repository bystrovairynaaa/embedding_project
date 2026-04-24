from sentence_transformers import SentenceTransformer

from embedders.base import BaseEmbedder
from config import SENTENCE_TRANSFORMER_MODEL


class SentenceTransformerEmbedder(BaseEmbedder):
    def __init__(self):
        self.model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            batch_size=64,
            show_progress_bar=True,
            normalize_embeddings=True,
        )
        return embeddings.tolist()

