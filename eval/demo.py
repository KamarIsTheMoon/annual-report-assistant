"""Run a standard set of questions on the reports in data/reports/ and save the answers.

    python -m eval.demo

Writes eval/results.md, ready to paste into the README "Results on real reports" section.
Check every answer against the PDF page before publishing: mark each one correct or wrong.
"""
from datetime import date
from pathlib import Path

from src.answer import answer
from src.extract import main as extract
from src.retrieve import Retriever

ROOT = Path(__file__).resolve().parents[1]


def run(questions_file: Path = ROOT / "eval" / "demo_questions.txt", out: Path = ROOT / "eval" / "results.md") -> str:
    passages = extract()
    if not passages:
        return ""
    retriever = Retriever(passages)
    files = sorted({p["source_file"] for p in passages})
    lines = [f"# Results on real reports ({date.today().isoformat()})", "", "Reports: " + ", ".join(files), "",
             "| Question | Answer (word for word from the report) | Source | Correct? |", "|---|---|---|---|"]
    for q in [l.strip() for l in questions_file.read_text(encoding="utf-8").splitlines() if l.strip()]:
        res = answer(q, retriever, k=1)
        src = res["sources"][0] if res["sources"] else None
        where = f"{src['company']} {src['year']}, p. {src['page']}" if src else "none"
        text = res["answer"].replace("|", "/")
        lines.append(f"| {q} | {text} | {where} | to check |")
    md = "\n".join(lines) + "\n"
    out.write_text(md, encoding="utf-8")
    print(md)
    print(f"Saved to {out.relative_to(ROOT)}. Open each cited page and replace 'to check' with yes or no.")
    return md


if __name__ == "__main__":
    run()
