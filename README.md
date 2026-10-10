# revenue-recognition

Ind AS 115 revenue recognition sub-ledger (draft). Design: `docs/design/revenue-platform.md`.
Source standard and guidance: `knowledge/ind-as-115/` (run `scripts/fetch_ind_as_115.sh`).

## Run the draft engine

```bash
python3 -m unittest discover -s tests -v
python3 -m revplat.cli examples/ssp_book.json examples/example_b_free_device_monthly.json
```

Standard library only (Python 3.9+).

## What exists (v0.1)

- Contract model: lines (performance obligations), invoices, enforceable transaction price.
- Versioned SSP book with segment-specific entries.
- Relative-SSP allocation with paise rounding that ties to the transaction price.
- Monthly recognition: point in time (hardware) and straight-line over time (data, SaaS).
- Per-contract monthly roll-forward: opening + billed - revenue = closing (contract liability if positive, contract asset if negative).

## Not yet built

Zoho import, event store and per-SIM activation dates, top-ups and breakage, contract modifications,
significant financing component, variable consideration and penalties (para 51AA), principal vs agent,
contract costs, daily proration, journal posting, disclosure reports, cohort aggregation for lakh-scale SIM volumes.
