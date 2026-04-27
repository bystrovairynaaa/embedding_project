from config import EMBEDDER


def get_embedder():
    if EMBEDDER == "sentence_transformer":
        from embedders.sentence_transformer_embedder import SentenceTransformerEmbedder

        return SentenceTransformerEmbedder()
    if EMBEDDER == "azure_openai":
        from embedders.azure_openai_embedder import AzureOpenAIEmbedder

        return AzureOpenAIEmbedder()
    raise ValueError(
        f"Unknown EMBEDDER value: '{EMBEDDER}'. Must be sentence_transformer | azure_openai"
    )


__all__ = ["get_embedder"]

