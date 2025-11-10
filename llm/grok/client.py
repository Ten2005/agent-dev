import os
from xai_sdk import Client
from xai_sdk.chat import user, system, assistant
from dotenv import load_dotenv
from llm.base import BaseLLM, Message, LLMResponse, Model, T
from typing import Type
from xai_sdk.tools import web_search, x_search

load_dotenv()


class GrokLLM(BaseLLM):
    def __init__(self):
        self.client = Client(
            api_key=os.getenv("XAI_API_KEY"),
            timeout=3600,
        )
        self.default_model = "grok-4-fast-reasoning"

    def _initialize_model(self, model: Model | None) -> str:
        return model.name if model else self.default_model

    def _append_messages_to_chat(self, chat, messages: list[Message]) -> None:
        """Append messages to chat with appropriate roles."""
        for message in messages:
            if message.role == "system":
                chat.append(system(message.content))
            elif message.role == "user":
                chat.append(user(message.content))
            elif message.role == "assistant":
                chat.append(assistant(message.content))

    def single_response(
        self, messages: list[Message], model: Model | None = None
    ) -> LLMResponse:
        model_name = self._initialize_model(model)
        chat = self.client.chat.create(
            model=model_name, tools=[web_search(), x_search()]
        )
        self._append_messages_to_chat(chat, messages)
        response = chat.sample()
        return LLMResponse(content=response.content)

    def structured_response(
        self, messages: list[Message], schema: Type[T], model: Model | None = None
    ) -> T:
        model_name = self._initialize_model(model)
        chat = self.client.chat.create(model=model_name)
        self._append_messages_to_chat(chat, messages)
        _, parsed_object = chat.parse(schema)
        return parsed_object
