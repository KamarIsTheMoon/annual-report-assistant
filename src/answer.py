"""Step 3: answer with the best sentence and always cite company, year and page.

Version 0.1 is extractive: the answer is the most relevant sentence taken word for word
from the report, so it can never invent a number. Version 0.2 will add a language model
that writes the answer from these passages only, still with citations.
"""
from .glossary import expand
from .retrieve import Retriever
from .text import split_sentences, tokenize


def best_sentence(question: str, text: str) -> str:
    q = set(tokenize(expand(question)))
    sentences = split_sentences(text) or [text]
    return max(sentences, key=lambda s: (len(q & set(tokenize(s))), any(c.isdigit() for c in s)))


def answer(question: str, retriever: Retriever, k: int = 3, **filters) -> dict:
    hits = retriever.search(question, k=k, **filters)
    if not hits:
        return {"question": question, "answer": "No relevant passage found in the reports.", "sources": []}
    top = hits[0]
    return {
        "question": question,
        "answer": best_sentence(question, top["text"]),
        "sources": [{"company": h["company"], "year": h["year"], "page": h["page"], "file": h["source_file"], "score": round(h["score"], 3)} for h in hits],
    }


def format_answer(result: dict) -> str:
    lines = [f"Q: {result['question']}", f"A: {result['answer']}"]
    for i, s in enumerate(result["sources"], 1):
        lines.append(f"   [{i}] {s['company']} {s['year']}, page {s['page']} ({s['file']}, score {s['score']})")
    return "\n".join(lines)
