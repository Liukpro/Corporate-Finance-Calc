# Corporate Finance Calc — Roadmap

## Vision
Build a Python tool that reads real financial statements, runs financial analysis
(cash flows, DCF valuation, benchmarking), and outputs structured, readable reports.

**Target use case:** junior analyst work in consulting, audit, financial advisory.
Specifically: balance sheet analysis, financial model support, DCF valuation,
due diligence, client-ready reports.

---

## Core Principle: Output Readability
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

## Core Principle: Separation of Concerns

Strict separation between:

- **Data Import** → reading external files
- **Data Cleaning** → technical fixes (NaN, types, formats)
- **Data Standardisation** → financial logic (building consistent variables)
- **Formulas** → pure mathematical functions
- **API / Output** → presentation layer

> Formulas must NEVER contain data cleaning or fallback logic.
