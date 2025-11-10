from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, TypeVar, Type
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class Message:
    role: Literal["system", "assistant", "user"]
    content: str


@dataclass
class Model:
    name: str


@dataclass
class LLMResponse:
    content: str


class BaseLLM(ABC):
    name: str

    @abstractmethod
    def single_response(
        self, messages: list[Message], model: Model | None = None
    ) -> LLMResponse:
        pass

    @abstractmethod
    def structured_response(
        self, messages: list[Message], schema: Type[T], model: Model | None = None
    ) -> T:
        pass
