import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from settings import Settings


class SearchService:
    def __init__(self, settings: Settings):
        self.settings = settings

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def search(self, query: str, limit: int = 3) -> list[str]:
        """Hämtar länkar från Google CSE, filtrerar på https och tar max limit."""
        params = {
            "key": self.settings.google_api_key,
            "cx": self.settings.google_cse_id,
            "q": query,
            "num": limit,
        }
        resp = requests.get(self.settings.google_api_url, params=params, timeout=20)
        if resp.status_code != 200:
            raise RuntimeError(f"Google CSE error {resp.status_code}: {resp.text}")
        data = resp.json()
        items = data.get("items", []) or []
        urls = []
        for item in items:
            url = item.get("link")
            if isinstance(url, str) and url.startswith("https://"):
                urls.append(url)
        return urls
