"""Ask a question from the command line.

    python -m src.ask "Quel est le chiffre d'affaires 2025 ?"
    python -m src.ask "What is the net debt?" --company Mutandis --year 2025
"""
import argparse

from .answer import answer, format_answer
from .retrieve import Retriever


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a question about the annual reports.")
    parser.add_argument("question")
    parser.add_argument("--company")
    parser.add_argument("--year")
    parser.add_argument("-k", type=int, default=3, help="number of sources to show")
    args = parser.parse_args()
    result = answer(args.question, Retriever.from_file(), k=args.k, company=args.company, year=args.year)
    print(format_answer(result))


if __name__ == "__main__":
    main()
