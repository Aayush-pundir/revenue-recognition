from dataclasses import dataclass
from decimal import Decimal
from typing import List

from .allocation import allocate
from .models import Contract
from .schedule import add_months, contract_revenue, month_key
from .ssp import SSPBook


@dataclass
class Row:
    month: str
    opening: Decimal        # +ve = contract liability, -ve = contract asset
    billed: Decimal
    revenue: Decimal
    closing: Decimal


def rollforward(contract: Contract, book: SSPBook) -> List[Row]:
    """Monthly contract balance roll-forward, net per contract (paras 105-107).

    closing = opening + billed - revenue
    Positive closing is a contract liability (deferred revenue);
    negative closing is a contract asset (revenue ahead of billing).
    """
    contract_date = min(l.start for l in contract.lines)
    alloc = allocate(contract, book, contract_date)
    rev = contract_revenue(contract, alloc)

    billed = {}
    for inv in contract.invoices:
        k = month_key(inv.date)
        billed[k] = billed.get(k, Decimal(0)) + inv.amount

    months = sorted(set(rev) | set(billed))
    last = months[-1]
    rows, bal, m = [], Decimal(0), months[0]
    while m <= last:
        b, r = billed.get(m, Decimal(0)), rev.get(m, Decimal(0))
        rows.append(Row(m, bal, b, r, bal + b - r))
        bal = bal + b - r
        m = add_months(m, 1)
    return rows
