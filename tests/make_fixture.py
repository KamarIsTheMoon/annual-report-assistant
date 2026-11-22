"""Builds tests/fixtures/Mutandis_2025_testfixture.pdf.

This is NOT the company's document. It is a short test file written for this project,
using figures published in Mutandis's 2025 press release (AMMC, 23/02/2026), placed on
known pages so the extraction and search can be tested automatically.
"""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

PAGES = [
    ["Fichier de test du projet annual-report-assistant (pas un document de la société).",
     "Activité 2025 du groupe Mutandis.",
     "Le chiffre d'affaires consolidé 2025 s'établit à 2 022 MDH, contre 2 117 MDH en 2024.",
     "Le pôle Hygiène réalise 761 MDH et le pôle Season USA 529 MDH.",
     "Le pôle Boissons recule à 258 MDH et les Produits de la mer à 474 MDH."],
    ["Rentabilité 2025.",
     "L'EBE (EBITDA) consolidé atteint 315 MDH en 2025, contre 351 MDH en 2024.",
     "Le résultat opérationnel courant s'élève à 205 MDH.",
     "Le résultat net part du groupe est de 126 MDH et le résultat net courant de 140 MDH."],
    ["Bilan et rémunération des actionnaires.",
     "La dette nette bancaire s'établit à 828 MDH au 31 décembre 2025, contre 851 MDH un an plus tôt.",
     "Les investissements corporels de l'exercice représentent 92 MDH.",
     "Un dividende de 10,5 dirhams par action est proposé."],
]


def build(out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out), pagesize=A4)
    for lines in PAGES:
        y = 780
        for line in lines:
            c.drawString(50, y, line)
            y -= 22
        c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    print(build(Path(__file__).parent / "fixtures" / "Mutandis_2025_testfixture.pdf"))
