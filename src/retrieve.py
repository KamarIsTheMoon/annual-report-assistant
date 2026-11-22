"""Step 2: find the passages most relevant to a question (TF-IDF, works in French and English)."""
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .glossary import expand
from .text import tokenize

ROOT = Path(__file__).resolve().parents[1]
PASSAGES = ROOT / "data" / "processed" / "passages.jsonl"


class Retriever:
    def __init__(self, passages: list[dict]):
        if not passages:
            raise ValueError("No passages: run `python -m src.extract` first.")
        self.passages = passages
        self.vectorizer = TfidfVectorizer(tokenizer=tokenize, lowercase=False, token_pattern=None, ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform([p["text"] for p in passages])

    @classmethod
    def from_file(cls, path: Path = PASSAGES) -> "Retriever":
        if not path.exists():
            from .extract import main as extract
            print("No extracted passages yet: running extraction first.")
            extract()
        with path.open(encoding="utf-8") as f:
            return cls([json.loads(line) for line in f])

    def search(self, question: str, k: int = 3, company: str | None = None, year: str | None = None) -> list[dict]:
        scores = cosine_similarity(self.vectorizer.transform([expand(question)]), self.matrix).ravel()
        ranked = []
        for idx in scores.argsort()[::-1]:
            p = self.passages[idx]
            if company and p["company"].lower() != company.lower():
                continue
            if year and p["year"] != str(year):
                continue
            if scores[idx] <= 0:
                break
            ranked.append({**p, "score": float(scores[idx])})
            if len(ranked) == k:
                break
        return ranked
