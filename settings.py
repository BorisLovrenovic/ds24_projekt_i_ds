import os
from dotenv import load_dotenv

load_dotenv()  # Läs in variabler från .env i aktuell mapp


def get_env(name: str, default: str | None = None, required: bool = False) -> str:
    """Hämtar miljövariabel. Stoppar tidigt om en obligatorisk variabel saknas."""
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"Environment variable {name} is required")
    return value or ""


class Settings:
    """Enkel konfig för den minimala/avskalade RAG."""

    def __init__(self):
        self.google_api_key = get_env("GOOGLE_API_KEY", required=True)
        self.google_cse_id = get_env("GOOGLE_CSE_ID", required=True)
        self.google_api_url = get_env(
            "GOOGLE_API_URL", "https://www.googleapis.com/customsearch/v1"
        )
        self.openai_api_key = get_env("OPENAI_API_KEY", required=True)
        self.qdrant_host = get_env("QDRANT_HOST", "localhost")
        self.qdrant_port = int(get_env("QDRANT_PORT", "6333"))
        self.aws_access_key = get_env("AWS_ACCESS_KEY", required=True)
        self.aws_secret_key = get_env("AWS_SECRET_KEY", required=True)
        self.aws_region = get_env("AWS_REGION", required=True)
        self.collection_name = get_env("QDRANT_COLLECTION", "enkel_rag")
        self.search_limit = int(get_env("SEARCH_LIMIT", "3"))
        self.rag_top_k = int(get_env("RAG_TOP_K", "3"))
