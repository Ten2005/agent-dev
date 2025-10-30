from openai import OpenAI
from dotenv import load_dotenv
import os
from nl_processor.embedding.base import BaseEmbedding, EmbeddingModel, Vectors

load_dotenv()


class OpenAIEmbedding(BaseEmbedding):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.default_model = "text-embedding-3-small"

    def embed(
        self, text: str | list[str], model: EmbeddingModel | None = None
    ) -> Vectors:
        model_name = model.name if model else self.default_model
        texts = [text] if isinstance(text, str) else text
        response = self.client.embeddings.create(input=texts, model=model_name)
        vectors = [item.embedding for item in response.data]

        return Vectors(vectors=vectors, model=model_name)
