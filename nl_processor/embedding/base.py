from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EmbeddingModel:
    name: str


@dataclass
class Vectors:
    vectors: list[list[float]]
    model: str


class BaseEmbedding(ABC):
    @abstractmethod
    def embed(
        self, text: str | list[str], model: EmbeddingModel | None = None
    ) -> Vectors:
        pass
