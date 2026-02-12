from openai import OpenAI
from settings import Settings


class ContentGenerator:
    def __init__(self, settings: Settings):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate(self, query: str, context: str) -> str:
        """Skickar fråga + kontext till modellen och får ett kort svar."""
        messages = [
            {
                "role": "system",
                "content": (
                    "Du är koncis och använder bara angivet kontext. "
                    "Om kontexten är otillräcklig, säg det."
                ),
            },
            {
                "role": "user",
                "content": f"Query: {query}\n\nContext:\n{context}\n\nAnswer:",
            },
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.4,
        )
        return response.choices[0].message.content
