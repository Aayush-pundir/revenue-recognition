import os
import unittest
from decimal import Decimal as D

from revplat.allocation import allocate
from revplat.ledger import rollforward
from revplat.loader import load_book, load_contract

EX = os.path.join(os.path.dirname(__file__), "..", "examples")
book = load_book(os.path.join(EX, "ssp_book.json"))


def contract(name):
    return load_contract(os.path.join(EX, name))


class ExampleA(unittest.TestCase):
    """Device + 12m plan, billed upfront: 1,500 hardware / 900 data."""

    def setUp(self):
        self.c = contract("example_a_bundle_upfront.json")

    def test_allocation(self):
        a = allocate(self.c, book, self.c.lines[0].start)
        self.assertEqual(a, {"L1": D("1500.00"), "L2": D("900.00")})

    def test_deferral(self):
        rows = rollforward(self.c, book)
        self.assertEqual(rows[0].revenue, D("1575.00"))   # 1500 + 75
        self.assertEqual(rows[0].closing, D("825.00"))    # contract liability
        self.assertEqual(rows[-1].closing, D("0"))
        self.assertEqual(sum(r.revenue for r in rows), D("2400.00"))


class ExampleB(unittest.TestCase):
    """Free device, committed 12m plan billed monthly: contract asset builds then unwinds."""

    def setUp(self):
        self.c = contract("example_b_free_device_monthly.json")

    def test_allocation(self):
        a = allocate(self.c, book, self.c.lines[0].start)
        self.assertEqual(a, {"L1": D("642.86"), "L2": D("1157.14")})

    def test_contract_asset(self):
        rows = rollforward(self.c, book)
        self.assertEqual(rows[0].revenue, D("739.29"))    # 642.86 + 96.43
        self.assertEqual(rows[0].closing, D("-589.29"))   # asset
        self.assertEqual(rows[-1].closing, D("0"))
        self.assertEqual(sum(r.revenue for r in rows), D("1800.00"))


if __name__ == "__main__":
    unittest.main()
