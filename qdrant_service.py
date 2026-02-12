import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from settings import Settings


class QdrantService:
    def __init__(self, settings: Settings):
        # Minimal wrapper runt Qdrant för att skapa/skriva/söka
        self.settings = settings
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port, timeout=30)
        self.collection = settings.collection_name
        self.vector_size = 1024
        self.ensure_collection()

    def ensure_collection(self):
        """Skapar collection om den saknas."""
        if self.client.collection_exists(self.collection):
            return
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=rest.VectorParams(size=self.vector_size, distance=rest.Distance.COSINE),
        )

    def upsert_points(self, points: list[dict]):
        """Sparar embeddings i Qdrant."""
        if not points:
            return
        qdrant_points = []
        for point in points:
            qdrant_points.append(
                rest.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=point.get("vector", []),
                    payload=point.get("payload", {}),
                )
            )
        self.client.upsert(collection_name=self.collection, points=qdrant_points)

    def search(self, query_vector: list[float], top_k: int = 3) -> list[dict]:
        """Hittar närmaste embeddings och returnerar bara payload."""
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=top_k,
        )
        payloads = []
        for r in results:
            payload = r.payload or {}
            payload["score"] = r.score
            payloads.append(payload)
        return payloads
