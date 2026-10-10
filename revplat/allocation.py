from decimal import Decimal, ROUND_HALF_UP
from typing import Dict

from .models import Contract
from .ssp import SSPBook

PAISE = Decimal("0.01")


def allocate(contract: Contract, book: SSPBook, contract_date) -> Dict[str, Decimal]:
    """Allocate the transaction price to lines on relative SSP (paras 73-80).

    Any rounding difference goes to the largest line so the total ties out.
    Discounts are spread across all lines (the default under paras 81-83).
    """
    ssp = {l.id: book.unit_ssp(l.product, contract.customer_type, contract_date) * l.qty
           for l in contract.lines}
    total_ssp = sum(ssp.values())
    out = {lid: (contract.transaction_price * s / total_ssp).quantize(PAISE, ROUND_HALF_UP)
           for lid, s in ssp.items()}
    diff = contract.transaction_price - sum(out.values())
    if diff:
        out[max(out, key=out.get)] += diff
    return out
