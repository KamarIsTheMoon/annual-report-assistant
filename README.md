# Annual Report Assistant

**Status:** version 0.1, working prototype. Next version planned for December 2026.

Ask a question about the annual reports of companies listed on the Casablanca Stock Exchange, in French or English, and get an answer **with the company, year and page it comes from**.

## The problem
Annual reports of Moroccan listed companies are long PDFs, mostly in French. An analyst can spend a long time looking for one figure. This assistant finds the passage that answers the question and always shows where it is, so every number can be checked.

## Example (v0.1, on the test file)
```
$ python -m src.ask "What is the net bank debt?"
Q: What is the net bank debt?
A: La dette nette bancaire s'établit à 828 MDH au 31 décembre 2025, contre 851 MDH un an plus tôt.
   [1] Mutandis 2025, page 3 (Mutandis_2025_testfixture.pdf, score 0.16)
   [2] Mutandis 2025, page 2 (Mutandis_2025_testfixture.pdf, score 0.127)
```

## How it works
1. **Extract** (`src/extract.py`): reads each PDF page by page, splits the text into passages and keeps the company, year and page number of each one. It falls back to a second PDF reader for pages with tables, and flags scanned pages that contain no text.
2. **Search** (`src/retrieve.py`): ranks passages with TF-IDF. Text is normalised (accents, case) and a small finance glossary (`src/glossary.py`) lets English questions find French passages, for example "net bank debt" finds "dette nette bancaire".
3. **Answer** (`src/answer.py`): returns the most relevant sentence **word for word** from the report, plus the sources. Version 0.1 never generates text, so it cannot invent a number.
4. **Evaluate** (`eval/run_eval.py`): checks whether the right page is found for a list of questions with known answers.
5. **Demo on real reports** (`eval/demo.py`): runs a standard set of analyst questions on every PDF in `data/reports/` and writes a results table to `eval/results.md`.

## Run it
```
pip install -r requirements.txt
# put PDFs in data/reports/ (see data/reports/README.md)
python -m src.extract
python -m src.ask "Quel est le chiffre d'affaires 2025 ?"
python -m eval.demo        # results table on your reports
python -m eval.run_eval    # accuracy on questions with known pages
python -m pytest tests     # automated tests
```

## Results so far
On the 3-page test file (6 questions, French and English), the right page is ranked first for all 6 questions, and the answer sentence is the correct one. This only shows the pipeline works: the test file is short and clean.

**Next:** results on full annual reports, with every answer checked by hand against the cited page, including the questions it gets wrong.

## Test file
`tests/fixtures/Mutandis_2025_testfixture.pdf` is **not a company document**. It is a short file written for this project with figures from Mutandis's 2025 press release (published through the AMMC on 23/02/2026), placed on known pages so the tests can check the results automatically.

## Roadmap
- [x] PDF extraction with page numbers
- [x] Search in French and English with a finance glossary
- [x] Extractive answers with citations
- [x] Evaluation script and automated tests
- [x] One-command demo that produces a results table on real reports
- [ ] Run on full annual reports of 5 listed companies
- [ ] Multilingual embeddings instead of TF-IDF
- [ ] Language model that writes the answer from the retrieved passages only, with citations
- [ ] Extract key figures automatically into a table for [casablanca-valuation-screener](https://github.com/KamarIsTheMoon/casablanca-valuation-screener)
- [ ] Simple web interface

## Repository
```
src/            extraction, search, answers, command line
eval/           test questions and evaluation script
tests/          automated tests and test file
data/reports/   PDFs go here (not committed)
```

© 2026 Kamar Maroihi. All rights reserved.
