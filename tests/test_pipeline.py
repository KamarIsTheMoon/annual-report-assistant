"""End to end test on the fixture: extraction keeps pages, search finds the right page.

    python -m pytest tests
"""
from pathlib import Path

from src.answer import answer
from src.extract import main as extract
from src.retrieve import Retriever
from tests.make_fixture import build

FIXTURES = Path(__file__).parent / "fixtures"


def retriever(tmp_path):
    build(FIXTURES / "Mutandis_2025_testfixture.pdf")
    passages = extract(FIXTURES, tmp_path / "passages.jsonl")
    return Retriever(passages)


def test_pages_are_kept(tmp_path):
    r = retriever(tmp_path)
    assert {p["page"] for p in r.passages} == {1, 2, 3}
    assert r.passages[0]["company"] == "Mutandis" and r.passages[0]["year"] == "2025"


def test_finds_the_right_page(tmp_path):
    r = retriever(tmp_path)
    cases = {
        "Quel est le chiffre d'affaires 2025 ?": 1,
        "What is the EBITDA?": 2,
        "Quelle est la dette nette bancaire ?": 3,
        "Dividende par action": 3,
        "résultat net part du groupe": 2,
    }
    for question, page in cases.items():
        assert r.search(question, k=1)[0]["page"] == page, question


def test_answer_cites_source(tmp_path):
    res = answer("Quelle est la dette nette ?", retriever(tmp_path))
    assert "828" in res["answer"]
    assert res["sources"][0]["page"] == 3
