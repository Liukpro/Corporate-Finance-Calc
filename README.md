# Corporate Finance Calc

A Python-based corporate finance analysis tool designed to replicate the workflow of a junior analyst in consulting, audit, and financial advisory.

The project evolves from a simple Streamlit demo into a full production tool that reads real financial statements, performs analysis (cash flows, valuation, benchmarking), and generates client-ready reports.

---

## Vision

Build a tool that:

* Reads structured financial statements (Excel)
* Performs corporate finance analysis (cash flows, DCF valuation, benchmarking)
* Outputs **clear, structured, and readable reports** suitable for non-technical stakeholders

**Target use case:**

* Financial analysis support
* Valuation (DCF)
* Due diligence
* Client-ready reporting

---

## Core Principle: Output Readability

This project is not just about correct calculations — it's about **clear communication**.

Every output must be understandable by someone with no coding background.

**Standards:**

* Consistent number formatting (2 decimals, thousand separators)
* Clear labels (no unexplained abbreviations)
* Plain-language warnings (no technical error messages)
* Structured outputs (tables with context, not raw numbers)
* Report-style presentation (ready to share with clients)

This applies to **every phase**, not just final reports.

---

## Current Features (Phase 1 — Demo)

### Cash Flow Calculations

* FCCNOGC
* RO-L
* FCGC
* FCID
* FCFR
* FCRf
* FCU
* FCE
* Variazione della Liquidità

Each metric can be calculated from:

* Direct input **or**
* Underlying components

Dependencies are handled automatically.

---

### NPV (Net Present Value)

* Variable number of periods
* Custom cash flows
* Fixed cost per period
* User-defined discount rate

---

## In Progress (Phase 1 Completion)

* Stock Evaluation (DDM, Gordon Growth Model)
* NPV comparison between projects
* Mortgage amortisation (French and Italian methods)
* Portfolio theory (risk/return, basic Markowitz)

---

## Project Architecture

### Current (Demo)

```
formulas.py     — pure financial logic
app.py          — Streamlit interface (demo only)
```

### Future (Production)

```
formulas.py     — core logic (expanded)
app.py          — demo (kept for visibility)
app2.py         — production tool (Excel → analysis → report)
tests/          — unit tests (pytest)
```

**Key rule:**
All financial logic stays in `formulas.py` — fully independent from any interface.

---

## Development Roadmap

### Phase 1 — Demo (current)

* Complete all financial modules
* Improve output readability in Streamlit
* Add warnings and contextual explanations

---

### Phase 2 — Excel Input (app2.py)

* Read financial statements via Excel (`pandas`, `openpyxl`)
* Map data automatically to calculations
* Handle:

  * Missing data
  * Formatting errors
  * Analytical anomalies

**CLI usage:**

```bash
python app2.py --file statement.xlsx
```

---

### Phase 3 — DCF Valuation

* Cash flow projections (3–5 years)
* WACC calculation (CAPM, cost of debt, capital structure)
* Terminal value (Gordon Growth)
* Enterprise → Equity value bridge
* Sensitivity analysis (WACC vs growth)
* Plain-language commentary on assumptions

---

### Phase 4 — Client-Ready Reports

* Excel output (formatted, structured)
* PDF reports (`reportlab`) including:

  * Executive summary
  * Key assumptions
  * Valuation results
  * Sensitivity tables
  * Warnings and anomalies
  * Appendix with calculations

Goal: output indistinguishable from analyst-prepared reports.

---

### Phase 5 — Market Data Integration (Optional)

* Market data via APIs (`yfinance`, ECB, Banca d’Italia)
* Comparable companies analysis
* Sector benchmarking
* Multiples (EV/EBITDA, P/E)

---

## Tech Stack

| Purpose         | Library       |
| --------------- | ------------- |
| Financial logic | Python, numpy |
| Data processing | pandas        |
| Excel I/O       | openpyxl      |
| PDF reports     | reportlab     |
| Market data     | yfinance      |
| Demo interface  | Streamlit     |
| Testing         | pytest        |

---

## Installation

```bash
git clone https://github.com/Liukpro/Corporate-Finance-Calc
cd Corporate-Finance-Calc
pip install -r requirements.txt
streamlit run app.py
```

---

## Project Structure

```
Corporate-Finance-Calc/
├── app.py          # Streamlit demo
├── app2.py         # Production tool (Phase 2+)
├── formulas.py     # Financial logic (core)
├── tests/          # Unit tests (planned)
├── ROADMAP.md      # Development roadmap
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Design Principles

* Separation of logic and interface
* Deterministic, testable functions
* Explicit error handling (`ValueError`)
* Scalable architecture (demo → production)
* Focus on **analyst usability**, not developer complexity

---

## Status

* Phase 1: in progress (demo + readability improvements)
* Phase 2+: planned

---

## License

This project is licensed under the terms specified in the LICENSE file.

