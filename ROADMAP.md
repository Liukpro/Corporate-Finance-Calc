# Corporate Finance Calc — Roadmap

## Vision
Build a Python tool that reads real financial statements, runs financial analysis
(cash flows, DCF valuation, benchmarking), and outputs structured, readable reports.

**Target use case:** junior analyst work in consulting, audit, financial advisory.
Specifically: balance sheet analysis, financial model support, DCF valuation,
due diligence, client-ready reports.

demo: https://corporate-finance-calc.streamlit.app/

---

## Core Principle: Output Readability
Everything in this project — from how results are displayed in the Streamlit demo
to how the final PDF is structured — must be readable by someone who is not a developer.

This means:
- Numbers formatted consistently (2 decimal places, thousand separators)
- Clear labels, no abbreviations without explanation
- Warnings and anomalies written in plain language, not error codes
- Output structured like a document a partner can send to a client
- Tables clean, logical, with context — not just raw numbers

This principle applies at every phase, not just Phase 4.

---

## Architecture — Current vs Future

### Current (demo)
```
formulas.py     — pure Python logic
app.py          — Streamlit interface (demo only)
```
Streamlit is used exclusively to have a graphic demo accessible online
via Streamlit Community Cloud. It is NOT the final product.

### Future (production)
```
formulas.py     — pure Python logic (keep and expand)
app.py          — Streamlit demo (keep for visibility/LinkedIn)
app2.py         — production tool: Excel in → analysis → readable report out
tests/          — pytest unit tests
```
`app2.py` is where the real product gets built.
No Streamlit dependency. Runs locally or on any server.

---

## Principles

### Keep
- `formulas.py` strictly separated from any interface
- `None` pattern for optional direct input
- `raise ValueError` for insufficient data
- `pytest` unit tests for every function in `formulas.py`
- **Output readability at every step**

### Review / Replace
- Streamlit → keep only as demo layer, never as core logic
- Manual number input → replace with Excel file reading (`pandas` + `openpyxl`)
- Raw number output → replace with formatted, labelled, contextualised results
- `st.success(f"result = {res}")` → structured output with context and warnings

---

## Phase 1 — Complete the Demo *(current)*
Finish all sections in `app.py`. Apply output readability already here:
format numbers, add context to results, warn on edge cases.

**Cash Flow**
- [x] FCCNOGC, RO-L, FCGC, FCID, FCFR, FCRf, FCU, FCE, Variazione Liquidità

**Valuation**
- [x] NPV
- [x] Zero Coupon Bond PV
- [ ] Stock Evaluation — DDM, Gordon Growth Model
- [ ] NPV Comparison — compare multiple projects side by side

**Other**
- [ ] Mortgage Amortisation — French and Italian method
- [ ] Portfolio — basic risk/return, Markowitz frontier

**Output readability checklist for every section:**
- [ ] Numbers formatted to 2 decimal places with thousand separators
- [ ] Results shown with label and unit, not just a number
- [ ] Edge cases flagged with plain language warnings
      (e.g. "NPV is negative — the project destroys value at this discount rate")

**Done when:** every sidebar section works and every result is readable
without knowing finance or coding.

---

## Phase 2 — Excel Input *(start of app2.py)*
Move from manual input to reading real financial statements.

- [ ] Design a standard Excel template (P&L, Cash Flow Statement, Balance Sheet)
- [ ] Read and parse the template with `pandas`
- [ ] Map Excel rows to `formulas.py` inputs automatically
- [ ] Handle missing and malformed data with plain language messages
      (e.g. "Column 'Revenue 2022' not found — check the template format")
- [ ] Handle analytically anomalous data with warnings
      (e.g. "EBITDA negative in 2 of the last 3 years — projections may be unreliable")
- [ ] CLI interface: `python app2.py --file statement.xlsx`

**Done when:** user runs a command with an Excel file and gets a readable
summary of all calculated cash flows, with warnings on any anomalies.

---

## Phase 3 — DCF Valuation
Build each component as you study it in Advanced Corporate Finance.

- [ ] Project free cash flows from historical data (3-5 year horizon)
- [ ] WACC — cost of equity via CAPM, cost of debt, capital structure weights
- [ ] Terminal value — Gordon Growth Model
- [ ] Enterprise value and equity value bridge
- [ ] Sensitivity analysis table — WACC vs terminal growth rate
- [ ] Contextual commentary on key drivers
      (e.g. "Valuation is sensitive to terminal growth rate —
      a 0.5% increase raises EV by X%")

**Done when:** `app2.py` outputs a full DCF valuation with sensitivity table
and plain language commentary on the main assumptions and risks.

---

## Phase 4 — Client-Ready Report Output
The final output must be a document a partner can send to a client unchanged.

- [ ] Export to Excel — formatted tables, clear headers, no raw data dumps (`openpyxl`)
- [ ] Export to PDF (`reportlab`):
  - Cover page
  - Executive summary in plain language
  - Key assumptions and inputs
  - DCF results with sensitivity table
  - Warnings and anomaly flags
  - Appendix with detailed calculations
- [ ] Consistent formatting throughout: fonts, colors, number format
- [ ] No developer language anywhere in the output

**Done when:** `python app2.py --file statement.xlsx --output report.pdf`
produces a document indistinguishable from one prepared manually by an analyst.

---

## Phase 5 — Market Data Integration
Cover benchmarking and comparable companies analysis.

- [ ] Pull market data — Yahoo Finance (`yfinance`), ECB, Banca d'Italia APIs
- [ ] Comparable companies — EV/EBITDA, P/E multiples from real market data
- [ ] Sector benchmarking — compare company ratios against sector averages
- [ ] Include benchmarks in the report with readable context
      (e.g. "EV/EBITDA of 8.2x vs sector median of 6.5x — company trades at a premium")

**Done when:** the report includes a benchmarking section with real market data
and plain language interpretation.

---

## Stack

| Purpose | Library | Phase |
|---|---|---|
| Financial logic | pure Python + numpy | all |
| Data manipulation | pandas | 2+ |
| Excel I/O | openpyxl | 2+ |
| PDF output | reportlab | 4 |
| Market data | yfinance | 5 |
| Interface (demo only) | Streamlit | 1 |
| Testing | pytest | all |

---

## Files

| File | Purpose | Status |
|---|---|---|
| `formulas.py` | All financial logic, no dependencies | active |
| `app.py` | Streamlit demo, LinkedIn/GitHub visibility | active |
| `app2.py` | Production tool, Excel in → report out | Phase 2 |
| `ROADMAP.md` | This file | active |
| `requirements.txt` | Dependencies | active |
| `tests/` | pytest unit tests | Phase 2 |

---

## Notes
- Output readability is not a Phase 4 concern — it starts in Phase 1
- Start `app2.py` at Phase 2 — never add Excel or report logic to `app.py`
- Implement Phase 3 components as you study them in the Master
- Phase 5 is optional — add after the Master if time allows
- The goal is not to impress developers — it is to produce something
  useful to an analyst who does not know Python
