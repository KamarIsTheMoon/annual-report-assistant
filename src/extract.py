"""Step 1: turn annual report PDFs into passages that keep their page number.

Usage:
    python -m src.extract

Reads every PDF in data/reports/ named COMPANY_YEAR_anything.pdf
(for example Mutandis_2025_communique.pdf) and writes data/processed/passages.jsonl.
"""
import json
import re
from pathlib import Path

from pypdf import PdfReader

try:
    import pdfplumber
except ImportError:  # optional, better on tables
    pdfplumber = None

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "data" / "reports"
OUT = ROOT / "data" / "processed" / "passages.jsonl"

WORDS_PER_PASSAGE = 120
OVERLAP = 30


def parse_name(pdf: Path) -> tuple[str, str]:
    """Company and year come from the file name: Mutandis_2025_xxx.pdf."""
    parts = pdf.stem.split("_")
    company = parts[0] if parts else pdf.stem
    year = next((p for p in parts if re.fullmatch(r"(19|20)\d\d", p)), "unknown")
    return company, year


def chunk_words(words: list[str]) -> list[str]:
    step = WORDS_PER_PASSAGE - OVERLAP
    return [" ".join(words[i:i + WORDS_PER_PASSAGE]) for i in range(0, max(len(words), 1), step) if words[i:i + WORDS_PER_PASSAGE]]


def extract_pdf(pdf: Path) -> list[dict]:
    company, year = parse_name(pdf)
    passages = []
    empty_pages = 0
    for page_number, text in enumerate(page_texts(pdf), start=1):
        words = text.split()
        if not words:
            empty_pages += 1
            continue
        for i, chunk in enumerate(chunk_words(words)):
            passages.append({
                "id": f"{pdf.stem}-p{page_number}-{i}",
                "company": company,
                "year": year,
                "source_file": pdf.name,
                "page": page_number,
                "text": chunk,
            })
    if empty_pages:
        print(f"  {pdf.name}: {empty_pages} page(s) with no text (scanned images?). OCR is on the roadmap.")
    return passages


def page_texts(pdf: Path) -> list[str]:
    """pypdf first; pdfplumber as a fallback for pages where pypdf finds nothing (often tables)."""
    texts = [page.extract_text() or "" for page in PdfReader(pdf).pages]
    if pdfplumber and any(not t.strip() for t in texts):
        with pdfplumber.open(pdf) as doc:
            texts = [t if t.strip() else (doc.pages[i].extract_text() or "") for i, t in enumerate(texts)]
    return texts


def main(reports_dir: Path = REPORTS, out: Path = OUT) -> list[dict]:
    pdfs = sorted(reports_dir.glob("*.pdf"))
    if not pdfs:
        print(f"No PDF found in {reports_dir}. See data/reports/README.md")
        return []
    passages = [p for pdf in pdfs for p in extract_pdf(pdf)]
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for p in passages:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    shown = out.relative_to(ROOT) if out.is_relative_to(ROOT) else out
    print(f"{len(pdfs)} report(s), {len(passages)} passages written to {shown}")
    return passages


if __name__ == "__main__":
    main()
