"""Measure how often the right page is among the sources returned.

    python -m eval.run_eval

Each row of eval/questions.csv gives a question and the page where the answer is.
"""
from pathlib import Path

import pandas as pd

from src.retrieve import Retriever

ROOT = Path(__file__).resolve().parents[1]


def evaluate(questions_csv: Path = ROOT / "eval" / "questions.csv", retriever: Retriever | None = None, k: int = 3) -> pd.DataFrame:
    retriever = retriever or Retriever.from_file()
    qs = pd.read_csv(questions_csv)
    rows = []
    for q in qs.itertuples():
        hits = retriever.search(q.question, k=k, company=q.company, year=str(q.year))
        pages = [h["page"] for h in hits]
        rows.append({"question": q.question, "expected_page": q.expected_page, "found_pages": pages,
                     "top1": bool(pages and pages[0] == q.expected_page), f"top{k}": q.expected_page in pages})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    res = evaluate()
    print(res.to_string(index=False))
    print(f"\nTop 1 accuracy: {res['top1'].mean():.0%} | Top 3 accuracy: {res['top3'].mean():.0%} on {len(res)} questions")
