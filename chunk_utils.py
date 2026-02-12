import tiktoken

encoding = tiktoken.get_encoding("o200k_base")


def chunk_text(text: str, max_tokens: int = 256) -> list[str]:
    """Delar text i mindre bitar så embeddings inte blir för stora."""
    if not isinstance(text, str) or len(text.strip()) == 0:
        raise ValueError("Input must be a non-empty string.")

    token_ids = encoding.encode(text)
    chunks = []
    i = 0

    while i < len(token_ids):
        chunk_token_ids = token_ids[i : i + max_tokens]
        decoded_text = encoding.decode(chunk_token_ids)
        if decoded_text.strip():
            chunks.append(decoded_text)
        i += max_tokens
    return chunks
