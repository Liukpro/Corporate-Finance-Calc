# Corporate Finance Calc

A Python tool that takes a company's financial data and produces a structured financial analysis — cash flows, valuation, and a readable report.

Built to automate what junior analysts do manually: reading balance sheets, calculating financial metrics, and producing output that can be used directly in a professional context.

---

## What it does today

The current version is a working demo, accessible online, that calculates the main corporate finance metrics studied in advanced finance courses:

**Cash Flows**
- FCCNOGC, RO-L, FCGC, FCID, FCFR, FCRf, FCU, FCE, Variazione di Liquidità

**Valuation**
- Net Present Value (NPV)
- Zero Coupon Bond present value

Each section accepts either direct values or individual components — the tool calculates what it can with the data available, and flags what is missing.

**Live demo:** https://corporate-finance-calc.streamlit.app

---

## Where it is going

The demo is the starting point. The goal is a tool that:

1. **Reads any Excel balance sheet** — not a fixed template, but real financial statements as companies actually produce them, with inconsistent labels and non-standard formats

2. **Interprets the data semantically** — maps rows like "fatturato netto" or "costi operativi" to the correct financial variables automatically, without manual input

3. **Runs the full analysis** — cash flows, DCF valuation, key ratios, multi-year comparison

4. **Produces a client-ready report** — structured PDF or Excel output with tables, commentary, and anomaly warnings, formatted to professional standards

The problem this solves is real: in consulting and audit, a significant portion of junior analyst time is spent moving data between tools and verifying that numbers are consistent. This tool automates that pipeline from start to finish.

---

## Examples

The `examples/` folder contains real balance sheets from Italian companies (public data) and the corresponding tool output. This shows what the tool produces on actual financial data, not just test numbers.

*(Examples will be added as the analysis features are completed)*

---

## Technical structure

The project is built with a strict separation between financial logic and interface:

- `formulas.py` — all financial calculations, no interface dependencies. Every function can be called independently and tested in isolation.
- `app.py` — Streamlit interface for the online demo
- `app2.py` *(in development)* — the production pipeline: Excel input → analysis → report output

---

## Status

| Feature | Status |
|---|---|
| Cash Flow (FCCNOGC, RO-L, FCGC, FCID, FCFR, FCRf, FCU, FCE, Var. Liquidità) | Complete |
| NPV | Complete |
| Bond Evaluation (Zero Coupon) | Complete |
| Stock Evaluation (DDM, Gordon Growth Model) | In progress |
| Mortgage Amortisation (French and Italian) | In progress |
| DCF valuation + WACC | Planned |
| NPV Comparison | In progress |
| Portfolio (risk/return, Markowitz frontier) | In progress |
| Excel input layer | Planned |
| PDF/Excel report output | Planned |
| Market data integration | Planned |

---

## License

Apache 2.0 — see LICENSE file.
