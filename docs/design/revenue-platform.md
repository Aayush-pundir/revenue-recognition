# Revenue recognition platform: design (draft v0.1)

Scope: Ind AS 115 sub-ledger for the four revenue streams: (1) hardware, (2) data subscription,
(3) SaaS platform fee, (4) intelligence/analytics. Standard references are paragraph numbers in
Ind AS 115 (see `knowledge/ind-as-115/`).

## 1. Facts established so far

| Topic | Answer | Design consequence |
|---|---|---|
| Billing / ERP | Zoho Books (the company's own instance, separate from the Zoho connector available to this assistant) | The platform is a **sub-ledger**: it reads invoices, credit notes and items from Zoho and posts revenue/deferral journals back. It cannot be tested against live data from this environment, so we need exported samples |
| Data plans | 1 or 2 years, differs by SIM and plan | Per-SIM term and activation date drive the clock. Plan terms are attributes of the contract line |
| Top-ups | Customers add data for a few days or a month | Short-term add-ons: separate contract at standalone price (para 20). Unused data may expire: see breakage (section 5) |
| Customer | OEM, fleet operator, or agency | Identify the customer per contract. An agency may be an **agent** of the fleet operator, not the customer (section 6) |
| Price list | None. SIM price is negotiated, so it differs by client | Contract price ≠ standalone selling price. SSP needs a policy (section 3) |

## 2. Architecture

```
Zoho Books ──► ingest ──► event store (append-only) ──► rules engine ──► ledger
(invoices,                activation/usage events       5-step model     (entries + balances)
 credit notes)            from connectivity platform                            │
                                                                                ├─► journals back to Zoho
                                                                                └─► disclosures / reports
```

- **Event store:** contract signed, shipped, SIM activated, usage, top-up, deactivation, modification, price change. Never edited. Corrections are new events.
- **Rules engine:** versioned accounting policy (distinct yes/no, SSP method, principal/agent, term rules) applied to events.
- **Ledger:** revenue, contract asset, contract liability (deferred revenue), unbilled revenue, capitalised contract costs, with a roll-forward per period.
- **Scale:** journals are posted per contract × performance obligation × month. Per-SIM rows are retained as evidence, not as separate schedules. Applying Ind AS 115 to a portfolio of similar contracts is allowed where the result is not materially different (para 4), and the portfolio basis is a documented policy.

## 3. Standalone selling price (SSP) with negotiated prices

Negotiated prices do **not** invalidate SSP. SSP is the price the entity would charge on a standalone sale (paras 76–80), estimated when no single observable price exists.

Proposed policy, to be agreed with the auditors:

1. **Observable prices first** (para 77): derive SSP from standalone sales of the item, grouped by segment (OEM / fleet / agency), volume band and term.
2. **Ranges, not points:** SSP is a range per group (for example median ± a set tolerance). A contract priced inside the range uses its own price. Outside it, the SSP is the group's median. The tolerance is a policy parameter. *This is common practice rather than a requirement of the standard.*
3. **Adjusted market assessment or expected cost plus margin** where there are too few standalone sales (para 79).
4. **Residual approach** only where SSP is highly variable or uncertain (para 79(c)).
5. Re-assess on a fixed schedule, and keep every SSP version with its effective dates and evidence.

## 4. Worked examples

**A. Device plus 12-month plan, billed upfront.** Price ₹2,400. SSP: device 2,000, plan 1,200 (total 3,200).
- Device: 2,400 × 2,000 / 3,200 = **₹1,500**, recognised at delivery.
- Plan: 2,400 × 1,200 / 3,200 = **₹900**, recognised at ₹75 a month over 12 months. At delivery, ₹900 sits as a contract liability.

**B. "Free" device with a 12-month committed plan, billed monthly.** Plan billed ₹150 a month (₹1,800); device is free (SSP 1,000); plan SSP ₹1,800.
- Total consideration 1,800 across SSPs of 2,800: device **₹642.86** (recognised at delivery, nothing billed, so a contract asset); plan **₹1,157.14**.
- Each month: bill 150, recognise 96.43 plan revenue, and release 53.57 of the contract asset. 96.43 + 53.57 = 150.
- This holds only if the 12-month commitment is **enforceable**. If the customer can cancel at any time with no penalty, the contract term is shorter (para 11) and there is no contract asset. The platform must capture termination terms for every contract.

## 5. Top-ups, expiry and modifications

- **Top-up for a few days or a month:** new distinct service at its own standalone price, so it is accounted for as a separate contract (para 20). Recognise over the validity period, or on usage if consumption is the better measure.
- **Unused prepaid data that expires:** breakage (paras B44–B47). Recognise expected breakage in proportion to usage if the entity expects to be entitled to it and a significant reversal is not probable. Otherwise recognise when the likelihood of use becomes remote. Needs a breakage estimate per plan type.
- **Adding SIMs to an existing contract:** modification (paras 18–21). If the added SIMs are distinct and priced at SSP, treat as a separate contract. Otherwise account for them prospectively or with a cumulative catch-up, per the rules in para 21.

## 6. Customer identification (OEM, fleet operator, agency)

- Decide for each contract whether the agency buys and resells (agency is the customer) or arranges sales on behalf of the fleet operator (agency is an agent, and the fleet operator is the customer).
- Margin, rebates or commissions paid to a customer are **consideration payable to a customer**, normally a reduction of revenue (paras 70–72). Commissions to an agent that is not a customer are contract costs (paras 91–94).
- Connectivity resold from a carrier needs a **principal vs agent** assessment (paras B34–B38). It decides gross vs net revenue.

## 6a. Indian specifics the platform must support

Penalties as per para 51AA, excise duty shown separately (109AA), reconciliation of revenue to contract price (126AA), and the unconditional right of return (B20AA).

## 7. Open items / inputs needed

1. A few **anonymised sample contracts and Zoho invoices** (OEM, fleet, agency) and a Zoho Books export of items and invoice lines. Do not share credentials.
2. Whether Zoho holds the **term, activation date and SIM count**, or whether these only exist in the connectivity platform.
3. **Cancellation / minimum-commitment terms** in standard contracts (decides example B).
4. Whether **SIM and data are distinct** under the company's policy (para 27). Auditor view required.
5. Whether **expiry of unused data** applies, and the historical usage needed to estimate breakage.
6. Who owns each policy parameter (SSP tolerance, breakage, portfolio approach) in finance.

## 8. Proposed build order

1. Data model and event store; ingest from Zoho exports.
2. SSP price book with versioning, and the allocation engine (examples A and B as test cases).
3. Monthly recognition run, contract balances and the deferred revenue roll-forward, load-tested at 5–10 lakh SIMs.
4. Top-ups, breakage, modifications.
5. Disclosure reports and journal posting back to Zoho.
