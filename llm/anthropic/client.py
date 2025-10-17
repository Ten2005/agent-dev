import anthropic
import os
from dotenv import load_dotenv

from llm.base import BaseLLM, Message, LLMResponse, Model, T

load_dotenv()


class AnthropicLLM(BaseLLM):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.default_model = "claude-haiku-4-5"

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
        anthropic_messages = self._convert_messages(messages)

        response = self.client.messages.create(
            model=model_name,
            max_tokens=1024,
            messages=anthropic_messages,
        )

        return LLMResponse(content=response.content[0].text)

    def structured_response(
        self, messages: list[Message], schema: type[T], model: Model | None = None
    ) -> T:
        model_name = self._initialize_model(model)
        anthropic_messages = self._convert_messages(messages)

        # Pydanticモデルから JSON Schemaを生成
        json_schema = schema.model_json_schema()

        # ツール定義を作成
        tools = [
            {
                "name": "output_formatter",
                "description": "Format the response according to the schema",
                "input_schema": json_schema,
            }
        ]

        # Claude APIを呼び出し
        response = self.client.messages.create(
            model=model_name,
            max_tokens=1024,
            tools=tools,
            tool_choice={"type": "tool", "name": "output_formatter"},
            messages=anthropic_messages,
        )

        # ツール呼び出しからJSONデータを抽出
        for content in response.content:
            if content.type == "tool_use" and content.name == "output_formatter":
                return schema(**content.input)

        raise ValueError("Tool response not found in Claude response")
