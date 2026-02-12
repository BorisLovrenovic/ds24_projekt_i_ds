import json
import boto3
from tenacity import retry, stop_after_attempt, wait_exponential
from settings import Settings
from chunk_utils import chunk_text


class BedrockEmbedder:
    def __init__(self, settings: Settings):
        # Enkel klient mot Titan-embeddings
        self.settings = settings
        self.model_id = "amazon.titan-embed-text-v2:0"
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=self.settings.aws_region,
            aws_access_key_id=self.settings.aws_access_key,
            aws_secret_access_key=self.settings.aws_secret_key,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Skickar textlistor till modellen och får embeddings tillbaka."""
        embeddings: list[list[float]] = []
        for text in texts:
            payload = {"inputText": text}
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(payload).encode("utf-8"),
                accept="application/json",
                contentType="application/json",
            )
            data = json.loads(response["body"].read().decode("utf-8"))
            embedding = data.get("embedding", [])
            embeddings.append(embedding)
        return embeddings


class EmbeddingService:
    def __init__(self, settings: Settings):
        self.embedder = BedrockEmbedder(settings)

    def embed_query(self, query: str) -> list[float]:
        """Embedda själva frågan för Qdrant-sök."""
        return self.embedder.embed([query])[0]

    def chunk_and_embed(self, docs: list[dict], max_tokens: int = 256) -> list[dict]:
        """Delar upp innehåll och skapar embeddings som kan sparas i Qdrant."""
        points: list[dict] = []
        for doc in docs:
            content = doc.get("content", "")
            source = doc.get("url", "")
            if not content.strip():
                continue
            chunks = chunk_text(content, max_tokens=max_tokens)
            vectors = self.embedder.embed(chunks)
            for text, vector in zip(chunks, vectors):
                if not isinstance(vector, list) or not vector:
                    continue
                points.append({
                    "vector": vector,
                    "payload": {
                        "content": text,
                        "source": source,
                    },
                })
        return points
