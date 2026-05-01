# Corporate Finance Calc - 

## What this project does

A web-based tool (Streamlit) that calculates standard financial metrics from manual inputs. No complex automation, no Excel parsing - just transparent formulas and immediate results.

### Current features

| Area | What it calculates |
|------|---------------------|
| Cash flows | FCCNOgc, FCGC, FCID, FCFR, FCRf, FCU, FCE, Liquidity variation |
| Profitability ratios | ROS, ROI, ROE |
| Investment valuation | NPV with fixed periodic costs |
| Bonds | Zero coupon (value and YTM), Coupon bonds |
| Stocks | Gordon growth model, No-growth model, VAOC |

Note: This is a calculator, not an automated analysis engine. All data must be entered manually. There is no cross-validation or automatic consistency checking.

---

## Calculation logic

All formulas are implemented as pure functions in `formule.py`, with:

- **Multiple calculation paths** - each metric can be computed in different ways (e.g., FCCNOgc from Revenue/Costs or from MOL)
- **Explicit error handling** - division by zero and insufficient data raise exceptions
- **Session state** - the app stores previous calculation results  
- **Calc demo on Streamlit:** https://corporate-finance-calc.streamlit.app/

---

**License** 
Please read License files

---

## Goal

Build a **deterministic corporate finance engine** that imports data from Excel and transforms financial statements into:
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

