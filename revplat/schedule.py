from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Tuple

from .models import Contract, OVER_TIME, POINT_IN_TIME

PAISE = Decimal("0.01")


def month_key(d) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def add_months(key: str, n: int) -> str:
    y, m = int(key[:4]), int(key[5:])
    idx = y * 12 + (m - 1) + n
    return f"{idx // 12:04d}-{idx % 12 + 1:02d}"


def line_schedule(line, amount: Decimal) -> List[Tuple[str, Decimal]]:
    """Revenue by month for one line. Monthly granularity, straight-line
    for over-time lines (stand-ready), last month takes the rounding."""
    first = month_key(line.start)
    if line.pattern == POINT_IN_TIME:
        return [(first, amount)]
    if line.pattern == OVER_TIME and line.months > 0:
        per = (amount / line.months).quantize(PAISE, ROUND_HALF_UP)
        rows = [(add_months(first, i), per) for i in range(line.months)]
        rows[-1] = (rows[-1][0], amount - per * (line.months - 1))
        return rows
    raise ValueError(f"Bad pattern for line {line.id}")


def contract_revenue(contract: Contract, allocation: Dict[str, Decimal]) -> Dict[str, Decimal]:
    rev: Dict[str, Decimal] = {}
    for line in contract.lines:
        for key, amt in line_schedule(line, allocation[line.id]):
            rev[key] = rev.get(key, Decimal(0)) + amt
    return rev
