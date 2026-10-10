# Ind AS 115 — Revenue from Contracts with Customers: source corpus

Primary sources for the product's subject-matter knowledge. Fetched from ICAI on 10 Oct 2026.

The documents are ICAI copyright ("All rights reserved"), and this repository is public, so the PDFs and
extracted text are **not committed**. Run the fetch script to populate them locally:

```bash
scripts/fetch_ind_as_115.sh
```

This writes the PDFs to `raw/` and `pdftotext -layout` output to `text/`. Both folders are gitignored.
The URLs are listed in [`sources.tsv`](sources.tsv).

## Documents

| # | Document | Authority | Edition / currency | Pages |
|---|----------|-----------|--------------------|-------|
| 01 | **Ind AS 115 — full text of the standard**: paras 1–129, Appendix A (defined terms), B (application guidance), C (effective date and transition), D–E (service concessions, formerly Appendix C of Ind AS 11), F (references), and Appendix 1 (differences from IFRS 15 / IFRIC 12 / SIC 29) | Mandatory, notified by MCA under the Companies (Ind AS) Rules, 2015 | ICAI Compendium of Ind AS **2025-26**, amended up to **G.S.R. 549(E), 13 Aug 2025** (see the amendment history below) | 98 |
| 02 | **ICAI Educational Material on Ind AS 115**: summary of the standard plus 78 FAQs with worked examples | ICAI Ind AS Implementation Group; non-mandatory guidance | Aug 2018, the only edition issued | 146 |
| 03 | **Compendium of ITFG Clarification Bulletins 1–17**, indexed by standard and including the Ind AS 115 issues | ICAI Ind AS Technical Facilitation Group; non-mandatory | Issued till Dec 2018 | 301 |
| 04 | ITFG Clarification Bulletin 19: mainly Ind AS 115 issues | ITFG | May 2019 | 12 |
| 05 | ITFG Clarification Bulletin 20: uses Ind AS 115 relative-SSP allocation by analogy | ITFG | Jun 2019 | 15 |
| 06 | ITFG Clarification Bulletin 22: scope of Ind AS 115 (free gifts / promotional items) | ITFG | Oct 2019 | 15 |
| 07 | ITFG Clarification Bulletin 23: deferred tax on Ind AS 115 transition adjustments | ITFG | Oct 2019, the last bulletin issued | 5 |

Bulletins 18 and 21 contain no Ind AS 115 content and are left out.

## Amendment history of the standard (per the footnote in doc 01)

- **G.S.R. 310(E), 28 Mar 2018**: Ind AS 115 notified, replacing Ind AS 11 and Ind AS 18. Effective for periods beginning on or after 1 Apr 2018.
- **G.S.R. 273(E), 30 Mar 2019**: several paragraphs substituted or omitted.
- **G.S.R. 419(E), 18 Jun 2021**: includes the insertion of Appendix D paras 28–28F.
- **G.S.R. 242(E), 31 Mar 2023**: editorial corrections.
- **G.S.R. 492(E), 12 Aug 2024**: consequential amendments from Ind AS 117 *Insurance Contracts* (scope).
- **G.S.R. 549(E), 13 Aug 2025**: editorial corrections.

Each changed paragraph carries an inline footnote in doc 01 that names the notification amending it.

## Indian carve-outs from IFRS 15 (Appendix 1 of doc 01)

These differences need specific handling in the product:

1. Penalties are removed from the variable-consideration examples in para 51. Para 51AA sets out their own treatment.
2. Para 109AA requires excise duty included in revenue to be presented separately.
3. Para 126AA requires a reconciliation of revenue recognised with the contracted price, listing each adjustment.
4. Para B20AA covers the transfer of control with an unconditional right of return.
5. The IFRS 15 transition paragraphs C1B, C8A and C9 and Appendix D paras 28/28E are deleted.

## Known gaps (not in this corpus)

- **IFRS 15 Illustrative Examples (Part B) and Basis for Conclusions (Part C).** ICAI hosts these under licence from the IFRS Foundation. They contain the IASB worked examples and are the most useful non-mandatory material. They are only served to Indian IP addresses, and the fetch from this environment was refused. From an Indian connection, download them from
  - Part B: https://www.icai.org/post/ifrs-partb-ifrss-2025-26 → "IFRS15_Revenue from Contracts with Customers"
  - Part C: https://www.icai.org/post/ifrs-partc-ifrss-2025-26 → same entry

  The licence terms restrict redistribution, so keep them out of this repo as well.
- **MCA gazette notifications.** mca.gov.in blocks automated access. Doc 01 already consolidates every notification.
- **ICAI Expert Advisory Committee (EAC) opinions** on revenue. These are spread across the EAC compendium volumes and are not collected here.
- **The withdrawn real-estate Guidance Note.** ICAI withdrew its Guidance Note on Real Estate Transactions (Ind AS) once Ind AS 115 took effect. It is intentionally excluded.
