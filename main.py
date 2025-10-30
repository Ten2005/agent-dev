from dotenv import load_dotenv
import os
import llm.anthropic.client
import llm.grok.client
import llm.gemini.client
import llm.openai.client
from llm.base import Message
from pydantic import BaseModel

load_dotenv()


class TestBool(BaseModel):
    bool: bool

def print_divider(text: str):
    print("\n" + "-" * 20 + "\n" + text + "\n" + "-" * 20 + "\n")

def main():
    print("Hello from agents dev!")

    print_divider("API Keys")
    api_keys = ["OPENAI", "ANTHROPIC", "GEMINI", "XAI"]
    for key in api_keys:
        print(
            f"{key} API Key: {'✓ Set' if os.getenv(f'{key}_API_KEY') else '✗ Not set'}"
        )

    prompt = "Say just Success"
    structured_prompt = "Say just True"
    llm_clients = {
        "anthropic": llm.anthropic.client.AnthropicLLM(),
        "grok": llm.grok.client.GrokLLM(),
        "gemini": llm.gemini.client.GeminiLLM(),
        "openai": llm.openai.client.OpenAILLM(),
    }

    print_divider("LLM Clients")
    for name, client in llm_clients.items():
        response = client.single_response([Message(role="user", content=prompt)])
        print(f"{name}: {response.content}")

    print_divider("Structured Response")
    for name, client in llm_clients.items():
        response = client.structured_response(
            [Message(role="user", content=structured_prompt)], schema=TestBool
        )
        print(f"{name}: {response.bool}")


if __name__ == "__main__":
    main()
