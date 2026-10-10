from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List

HARDWARE = "hardware"
DATA = "data"
SAAS = "saas"
ANALYTICS = "analytics"

POINT_IN_TIME = "point_in_time"
OVER_TIME = "over_time"


@dataclass
class Line:
    """One distinct good or service in a contract (a performance obligation)."""
    id: str
    product: str            # key into the SSP book, e.g. "dashcam", "data-12m"
    stream: str             # hardware / data / saas / analytics
    qty: int
    pattern: str            # point_in_time or over_time
    start: date             # delivery date, or service start date
    months: int = 0         # service term in months; over_time only


@dataclass
class Invoice:
    date: date
    amount: Decimal


@dataclass
class Contract:
    id: str
    customer: str
    customer_type: str      # oem / fleet / agency
    transaction_price: Decimal  # enforceable fixed consideration, after discounts
    lines: List[Line]
    invoices: List[Invoice] = field(default_factory=list)
