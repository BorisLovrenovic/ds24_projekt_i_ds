import json
import trafilatura


class ContentExtractor:
    def __init__(self, max_content_length: int = 5000):
        self.max_content_length = max_content_length

    def extract(self, url: str) -> str:
        """Hämtar sida och tar bara textinnehållet via trafilatura."""
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return ""

        data = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_images=False,
            output_format="json",
            include_tables=False,
            with_metadata=False,
        )
        if not data:
            return ""

        json_data = json.loads(data)
        content = json_data.get("text", "")
        if not content:
            return ""

        trimmed = content.strip()
        if len(trimmed) > self.max_content_length:
            trimmed = trimmed[: self.max_content_length]
        return trimmed
