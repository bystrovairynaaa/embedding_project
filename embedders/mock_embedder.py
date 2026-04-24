import numpy as np

from embedders.base import BaseEmbedder
from config import MOCK_EMBEDDING_DIM


class MockEmbedder(BaseEmbedder):
    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = np.random.randn(len(texts), MOCK_EMBEDDING_DIM)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        vectors = vectors / norms
        return vectors.tolist()

