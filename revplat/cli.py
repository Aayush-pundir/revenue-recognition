import sys

from .allocation import allocate
from .ledger import rollforward
from .loader import load_book, load_contract


def main(argv):
    if len(argv) != 3:
        print("usage: python -m revplat.cli <ssp_book.json> <contract.json>")
        return 2
    book, c = load_book(argv[1]), load_contract(argv[2])
    alloc = allocate(c, book, min(l.start for l in c.lines))
    print(f"Contract {c.id}  customer={c.customer} ({c.customer_type})  price={c.transaction_price}")
    for l in c.lines:
        print(f"  allocated {l.id:<10} {l.product:<12} {alloc[l.id]:>12}")
    print(f"\n{'month':<8}{'opening':>12}{'billed':>12}{'revenue':>12}{'closing':>12}  position")
    for r in rollforward(c, book):
        pos = "liability" if r.closing > 0 else "asset" if r.closing < 0 else "-"
        print(f"{r.month:<8}{r.opening:>12}{r.billed:>12}{r.revenue:>12}{r.closing:>12}  {pos}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
