from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Type
from llm.base import BaseLLM, Message, LLMResponse, Model, T

load_dotenv()


class OpenAILLM(BaseLLM):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.default_model = "gpt-5"

    def _initialize_model(self, model: Model | None) -> str:
        return model.name if model else self.default_model

    def _convert_messages(self, messages: list[Message]) -> list[dict]:
        return [
            {"role": message.role, "content": message.content} for message in messages
        ]

    def single_response(
        self, messages: list[Message], model: Model | None = None
    ) -> LLMResponse:
        model_name = self._initialize_model(model)
        openai_messages = self._convert_messages(messages)

        response = self.client.responses.create(
            model=model_name,
            tools=[{"type": "web_search"}],
            input=openai_messages,
        )

        return LLMResponse(content=response.output_text)

    def structured_response(
        self, messages: list[Message], schema: Type[T], model: Model | None = None
    ) -> T:
        model_name = self._initialize_model(model)
        openai_messages = self._convert_messages(messages)

        response = self.client.responses.parse(
            model=model_name,
            tools=[{"type": "web_search"}],
            input=openai_messages,
            text_format=schema,
        )

        return response.output_parsed
