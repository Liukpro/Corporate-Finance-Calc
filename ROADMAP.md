# Corporate Finance Calc — Roadmap

## Output Readability
Everything in this project — from how results are displayed in the Streamlit demo
to how the final output is structured — must be readable by a non-developer.

This means:
- Numbers formatted consistently (2 decimal places, thousand separators)
- Clear labels, no unexplained abbreviations
- Warnings written in plain language, not error codes
- Output structured like a client-ready document
- Tables clean, logical, contextualised

This principle applies at every phase.

---

## Separation of Concerns

Strict separation between:

- **Data Import** → reading external files
- **Data Cleaning** → technical fixes (NaN, types, formats)
- **Data Standardisation** → financial logic (building consistent variables)
- **Formulas** → pure mathematical functions
- **API / Output** → presentation layer

> Formulas must NEVER contain data cleaning or fallback logic.

---

### Phase 1 — Formulas + Demo (current)
- Build and validate all financial formulas
- Remove fallback logic
- Add unit tests
- Use Streamlit only for testing


### Phase 2 — Data Pipeline
- Read Excel financial statements (`pandas`)
- Clean data (missing values, formats)
- Standardise financial variables
- Validate inputs and flag anomalies


### Phase 3 — API Layer (optional but recommended)
- Build API using :contentReference[oaicite:0]{index=0}
- One endpoint per calculation
- Structured JSON input/output


### Phase 4 — DCF Valuation
- Forecast cash flows
- WACC (CAPM + cost of debt)
- Terminal value (Gordon Growth)
- Sensitivity analysis
- Plain-language interpretation


### Phase 5 — Output Layer
- Currently in evaluation

### Phase 6 — Market Data
- Currently in evaluation

---

## Status

| Feature | Status |
|---|---|
| Cash Flow calculations | Refactoring (towards deterministic logic) |
| NPV | Complete |
| Bond evaluation (Zero Coupon) | Complete |
| Stock valuation (DDM, Gordon Growth) | In progress |
| Mortgage amortisation | In progress |
| Portfolio (Markowitz) | In progress |
| Excel input layer | Planned |
| Data cleaning & standardisation | Planned |
| API layer | Planned |
| DCF valuation | Planned |
| Output (Power BI / PDF) | Evaluating |
| Market data integration | Evaluating |
