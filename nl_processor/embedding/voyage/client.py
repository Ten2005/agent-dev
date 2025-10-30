import voyageai
from dotenv import load_dotenv
import os
from nl_processor.embedding.base import BaseEmbedding, EmbeddingModel, Vectors

load_dotenv()


class VoyageEmbedding(BaseEmbedding):
    def __init__(self):
        self.client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
        self.default_model = "voyage-3.5"

    def embed(
        self, text: str | list[str], model: EmbeddingModel | None = None
    ) -> Vectors:
        model_name = model.name if model else self.default_model

        texts = [text] if isinstance(text, str) else text
        result = self.client.embed(texts, model=model_name, input_type="document")
        vectors = result.embeddings

        return Vectors(vectors=vectors, model=model_name)
