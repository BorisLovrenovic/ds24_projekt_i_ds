import re

# Tillåt bara enkla tecken för att undvika skräp i frågan
ALLOWED_CHARS = re.compile(r"^[a-zA-Z0-9\s\.,!?\'\":;\-]+$")
# Blocklist mot SQL/JS-mönster
SQL_INJECTION_PATTERNS = re.compile(
    r"(\b(union|select|insert|delete|drop|alter|exec|script|--|;|\bjavascript:)\b)|[<>{}]",
    re.IGNORECASE,
)


def sanitize_input(query: str) -> str:
    """Rensar och validerar enkel användarinput."""
    query = re.sub(r"\s+", " ", query.strip())
    if not query:
        raise ValueError("Query cannot be empty")
    if len(query) > 500:
        raise ValueError("Query too long (max 500 characters)")
    if len(query) < 3:
        raise ValueError("Query too short (min 3 characters)")
    if not ALLOWED_CHARS.match(query):
        raise ValueError("Query contains invalid characters")
    if SQL_INJECTION_PATTERNS.search(query):
        raise ValueError("Query contains prohibited patterns")
    return query
