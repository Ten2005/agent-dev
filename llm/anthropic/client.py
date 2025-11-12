import anthropic
import os
from dotenv import load_dotenv
from llm.base import BaseLLM, Message, LLMResponse, Model, T

load_dotenv()


class AnthropicLLM(BaseLLM):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.default_model = "claude-sonnet-4-5"
        self.name = "anthropic"

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
            tools=[
                {"type": "web_search_20250305", "name": "web_search", "max_uses": 5}
            ],
        )
        return LLMResponse(content=response.content[0].text)

    def structured_response(
        self, messages: list[Message], schema: type[T], model: Model | None = None
    ) -> T:
        model_name = self._initialize_model(model)
        anthropic_messages = self._convert_messages(messages)
        json_schema = schema.model_json_schema()
        tools = [
            {
                "name": "output_formatter",
                "description": "Format the response according to the schema",
                "input_schema": json_schema,
            },
            {"type": "web_search_20250305", "name": "web_search", "max_uses": 5},
        ]
        response = self.client.messages.create(
            model=model_name,
            max_tokens=1024,
            tools=tools,
            tool_choice={"type": "tool", "name": "output_formatter"},
            messages=anthropic_messages,
        )
        for content in response.content:
            if content.type == "tool_use" and content.name == "output_formatter":
                return schema(**content.input)
        raise ValueError("Tool response not found in Claude response")
