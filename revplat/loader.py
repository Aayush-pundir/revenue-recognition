import json
from datetime import date
from decimal import Decimal

from .models import Contract, Invoice, Line
from .ssp import SSPBook, SSPEntry


def _d(s):
    return date.fromisoformat(s)


def load_book(path) -> SSPBook:
    with open(path) as f:
        raw = json.load(f)
    return SSPBook([SSPEntry(e["product"], Decimal(e["unit_ssp"]), _d(e["effective_from"]),
                             e.get("segment", "*")) for e in raw])


def load_contract(path) -> Contract:
    with open(path) as f:
        c = json.load(f)
    lines = [Line(l["id"], l["product"], l["stream"], l["qty"], l["pattern"],
                  _d(l["start"]), l.get("months", 0)) for l in c["lines"]]
    invs = [Invoice(_d(i["date"]), Decimal(i["amount"])) for i in c.get("invoices", [])]
    return Contract(c["id"], c["customer"], c["customer_type"],
                    Decimal(c["transaction_price"]), lines, invs)
