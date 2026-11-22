"""Small English to French finance glossary.

Reports are mostly in French. Without this, an English question like "net bank debt"
cannot match "dette nette bancaire". Version 0.2 will replace this with multilingual embeddings.
"""
EN_TO_FR = {
    "revenue": "chiffre affaires", "sales": "chiffre affaires ventes", "turnover": "chiffre affaires",
    "debt": "dette endettement", "bank": "bancaire", "dividend": "dividende", "share": "action",
    "per share": "par action", "net income": "resultat net", "profit": "resultat benefice",
    "earnings": "resultat", "ebitda": "ebe ebitda", "operating income": "resultat operationnel",
    "capex": "investissements", "investment": "investissements", "cash": "tresorerie",
    "equity": "capitaux propres", "risk": "risque risques", "margin": "marge",
    "beverages": "boissons", "seafood": "produits mer", "hygiene": "hygiene",
}


def expand(question: str) -> str:
    q = question.lower()
    extra = [fr for en, fr in EN_TO_FR.items() if en in q]
    return question + (" " + " ".join(extra) if extra else "")
