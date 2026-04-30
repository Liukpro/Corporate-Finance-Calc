# Corporate Finance Engine — System Roadmap (Architecture v2)

**Demo on Streamlit:** https://corporate-finance-calc.streamlit.app/

---

**License** 
Please read License files

---

## Goal

Build a **deterministic corporate finance engine** that transforms financial statements into:
- profitability metrics
- cash flow analysis
- valuation outputs (NPV, bonds)
- a lot more

All results must be:
- readable for non-developers
- numerically consistent
- structured for reporting (Streamlit UI)

---

## Core Design Principle

### Strict Separation of Concerns

- **data_layer.py** → reads and structures raw Excel data
- **validation.py** → checks consistency, fixes formats, normalises units
- **financial_schema.py** → defines variables and naming conventions (no logic)
- **multi_path_DAG.py** → defines financial formulas (pure math functions only)
- **resolver.py** → selects computation paths and builds results
- **streamlit_app.py** → final report and user interface

> No financial logic outside DAG and resolver   
> No ambiguity in variable naming

