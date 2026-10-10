from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List


@dataclass
class SSPEntry:
    product: str
    unit_ssp: Decimal
    effective_from: date
    segment: str = "*"      # customer type, or * for any
    low: Decimal = None     # observed range, used only for flagging
    high: Decimal = None


class SSPBook:
    """Versioned standalone selling prices (paras 76-80).

    Lookup picks the latest entry effective on the contract date, preferring
    a segment-specific entry over the wildcard.
    """

    def __init__(self, entries: List[SSPEntry]):
        self.entries = entries

    def unit_ssp(self, product: str, segment: str, on: date) -> Decimal:
        live = [e for e in self.entries
                if e.product == product and e.effective_from <= on
                and e.segment in (segment, "*")]
        if not live:
            raise KeyError(f"No SSP for {product!r} ({segment}) on {on}")
        live.sort(key=lambda e: (e.segment == segment, e.effective_from))
        return live[-1].unit_ssp
