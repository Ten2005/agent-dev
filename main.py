from dotenv import load_dotenv
import os
import llm.anthropic.client
import llm.gemini.client
import llm.grok.client
import llm.openai.client
from llm.base import Message
from pydantic import BaseModel
import nl_processor.embedding.openai.client
import nl_processor.embedding.gemini.client
import nl_processor.embedding.voyage.client
from nl_processor.embedding.base import BaseEmbedding

load_dotenv()


class TestBool(BaseModel):
    bool: bool


def print_divider(text: str):
    print("\n" + "-" * 20 + "\n" + text + "\n" + "-" * 20 + "\n")


def main(
    api_key: bool = False,
    call: bool = False,
    structured: bool = False,
    embedding: bool = False,
):
    print("Hello from agents dev!")
    if api_key:
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
        "gemini": llm.gemini.client.GeminiLLM(),
        "grok": llm.grok.client.GrokLLM(),
        "openai": llm.openai.client.OpenAILLM(),
    }
    if call:
        print_divider("LLM Clients")
        for name, client in llm_clients.items():
            llm_response = client.single_response(
                [Message(role="user", content=prompt)]
            )
            print(f"{name}: {llm_response.content}")

    if structured:
        print_divider("Structured Response")
        for name, client in llm_clients.items():
            structured_response: TestBool = client.structured_response(
                [Message(role="user", content=structured_prompt)], schema=TestBool
            )
            print(f"{name}: {structured_response.bool}")

    if embedding:
        print_divider("Embedding")
        embedding_clients: dict[str, BaseEmbedding] = {
            "openai": nl_processor.embedding.openai.client.OpenAIEmbedding(),
            "gemini": nl_processor.embedding.gemini.client.GeminiEmbedding(),
            "voyage": nl_processor.embedding.voyage.client.VoyageEmbedding(),
        }
        for name, embedding_client in embedding_clients.items():
            embedding_response = embedding_client.embed(text="Hello, world!")
            print(f"{name}: {len(embedding_response.vectors[0])}")


if __name__ == "__main__":
    main(api_key=True, call=True, structured=True, embedding=True)
