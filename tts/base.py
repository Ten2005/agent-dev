from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Model:
    name: str


@dataclass
class TTSResponse:
    audio: bytes


class BaseTTS(ABC):
    @abstractmethod
    def generate_audio(self, text: str, model: Model | None = None) -> TTSResponse:
        pass
