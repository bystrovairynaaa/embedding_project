from abc import ABC, abstractmethod


class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Input:  list of N strings
        Output: list of N vectors (each vector is a list of floats)
        All vectors must have the same dimension.
        """
        raise NotImplementedError()

