from google import genai
from dotenv import load_dotenv
import os
from nl_processor.embedding.base import BaseEmbedding, EmbeddingModel, Vectors

load_dotenv()


class GeminiEmbedding(BaseEmbedding):
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.default_model = "gemini-embedding-001"

    def embed(
        self, text: str | list[str], model: EmbeddingModel | None = None
    ) -> Vectors:
        model_name = model.name if model else self.default_model
        texts = [text] if isinstance(text, str) else text
        response = self.client.models.embed_content(model=model_name, contents=texts)
        vectors = [item.values for item in response.embeddings]

        return Vectors(vectors=vectors, model=model_name)
