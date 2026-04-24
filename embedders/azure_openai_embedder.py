import time

from openai import AzureOpenAI

from embedders.base import BaseEmbedder
from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_BATCH_SIZE,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
)


class AzureOpenAIEmbedder(BaseEmbedder):
    def __init__(self):
        if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY:
            raise ValueError(
                "Missing Azure OpenAI credentials. "
                "Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY env vars."
            )
        self.client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        all_vectors: list[list[float]] = []
        for i in range(0, len(texts), AZURE_OPENAI_BATCH_SIZE):
            batch = texts[i : i + AZURE_OPENAI_BATCH_SIZE]
            response = self.client.embeddings.create(
                input=batch,
                model=AZURE_OPENAI_DEPLOYMENT,
            )
            batch_vectors = [
                item.embedding for item in sorted(response.data, key=lambda x: x.index)
            ]
            all_vectors.extend(batch_vectors)
            if i + AZURE_OPENAI_BATCH_SIZE < len(texts):
                time.sleep(0.2)
        return all_vectors

