from typing import List
from settings import Settings
from sanitization import sanitize_input
from search_service import SearchService
from extractor import ContentExtractor
from embedding_service import EmbeddingService
from qdrant_service import QdrantService
from content_generator import ContentGenerator


class SimpleRAG:
    def __init__(self, settings: Settings | None = None):
        # Initiera alla enkla delkomponenter
        self.settings = settings or Settings()
        self.search_service = SearchService(self.settings)
        self.extractor = ContentExtractor()
        self.embedder = EmbeddingService(self.settings)
        self.qdrant = QdrantService(self.settings)
        self.generator = ContentGenerator(self.settings)

    def _extract_sources(self, urls: List[str]) -> List[dict]:
        """Hämtar textinnehåll från varje URL."""
        docs: List[dict] = []
        for url in urls:
            content = self.extractor.extract(url)
            if content:
                docs.append({"url": url, "content": content})
        return docs

    def _build_context(self, payloads: List[dict]) -> str:
        """Slår ihop payload-texter till en enkel kontextsträng."""
        parts = []
        for p in payloads:
            text = p.get("content", "")
            if text:
                parts.append(text)
        return "\n\n".join(parts)

    def run(self, query: str) -> str:
        """Kör hela minimala RAG-flödet och returnerar svar."""
        cleaned_query = sanitize_input(query)

        urls = self.search_service.search(cleaned_query, limit=self.settings.search_limit)
        docs = self._extract_sources(urls)
        points = self.embedder.chunk_and_embed(docs)
        self.qdrant.upsert_points(points)

        query_vector = self.embedder.embed_query(cleaned_query)
        hits = self.qdrant.search(query_vector, top_k=self.settings.rag_top_k)
        context = self._build_context(hits)

        if not context.strip():
            return "Hittade inget användbart innehåll för din fråga."

        return self.generator.generate(cleaned_query, context)
