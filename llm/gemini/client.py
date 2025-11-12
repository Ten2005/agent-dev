from google import genai
from dotenv import load_dotenv
import os
import json
from llm.base import BaseLLM, Message, LLMResponse, Model, T
from typing import Type

load_dotenv()


class GeminiLLM(BaseLLM):
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.default_model = "gemini-2.5-flash-lite"
        self.name = "gemini"

    def _initialize_model(self, model: Model | None) -> str:
        return model.name if model else self.default_model

    def _convert_messages(self, messages: list[Message]) -> list[dict]:
        return [
            {
                "role": "model" if message.role == "assistant" else message.role,
                "parts": [{"text": message.content}],
            }
            for message in messages
        ]

    def single_response(
        self, messages: list[Message], model: Model | None = None
    ) -> LLMResponse:
        model_name = self._initialize_model(model)
        gemini_messages = self._convert_messages(messages)
        response = self.client.models.generate_content(
            model=model_name,
            contents=gemini_messages,
        )
        return LLMResponse(content=response.text)

    def structured_response(
        self, messages: list[Message], schema: Type[T], model: Model | None = None
    ) -> T:
        model_name = self._initialize_model(model)
        gemini_messages = self._convert_messages(messages)
        json_schema = schema.model_json_schema()
        response = self.client.models.generate_content(
            model=model_name,
            contents=gemini_messages,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=json_schema,
            ),
        )
        response_json = json.loads(response.text)
        return schema(**response_json)
