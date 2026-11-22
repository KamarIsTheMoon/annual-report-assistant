"""Text helpers shared by extraction and retrieval."""
import re
import unicodedata

FRENCH_STOPWORDS = {
    "le", "la", "les", "un", "une", "des", "du", "de", "d", "l", "et", "en", "a", "au", "aux",
    "est", "sont", "quel", "quelle", "quels", "quelles", "pour", "par", "sur", "dans", "ce",
    "cette", "ces", "qui", "que", "quoi", "comment", "son", "sa", "ses", "leur", "leurs",
}
ENGLISH_STOPWORDS = {
    "the", "a", "an", "of", "and", "in", "to", "is", "are", "what", "which", "how", "for",
    "on", "its", "their", "was", "were", "by", "with", "did",
}
STOPWORDS = FRENCH_STOPWORDS | ENGLISH_STOPWORDS


def normalize(text: str) -> str:
    """Lowercase, remove accents and collapse spaces, so 'Chiffre d'Affaires' matches 'chiffre d affaires'."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().replace("’", " ").replace("'", " ")
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+(?:[.,][0-9]+)?", normalize(text)) if t not in STOPWORDS]


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?;])\s+|\n+", text)
    return [p.strip() for p in parts if len(p.strip()) > 20]
