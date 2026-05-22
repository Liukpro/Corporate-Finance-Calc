# Corporate Finance Calc

## What this project does

A web-based tool (Streamlit) that calculates standard financial metrics from manual inputs. No complex automation, no Excel parsing - just transparent formulas and immediate results.

---

## Calculation logic

All formulas are implemented as pure functions in `formulas.py`, with:

- **Multiple calculation paths** - each metric can be computed in different ways (e.g., FCCNOgc from Revenue/Costs or from MOL)
- **Explicit error handling** - division by zero and insufficient data raise exceptions
- **Session state** - the app stores previous calculation results  
- **Demo on Streamlit:** https://corporate-finance-calc.streamlit.app/
## **Warning**: to access the demo press "Yes, get this app back up!" after entering the given url. 

---

### Current features

| Area | What it calculates |
|------|---------------------|
| Cash flows | FCCNOgc, FCGC, FCID, FCFR, FCRf, FCU, FCE, Liquidity variation |
| Profitability ratios | ROS, ROI, ROE |
| Prospective Analysis | Operating Free Cash Flow (after working capital changes) |
| Investment valuation | NPV with fixed periodic costs |
| Bonds | Zero coupon (value and YTM), Coupon bonds |
| Stocks | Gordon growth model, No-growth model, VAOC |

Note: This is a calculator, not an automated analysis engine. All data must be entered manually. There is no cross-validation or automatic consistency checking.

---

**License** 
Please read License files

---

## System Status and Other Important Information, read carefully.

This project is not a finished application, results may be subject to errors. Do not rely only on the data shown.

This project is entirely based on "Finanza Aziendale" a university-taught course at the Università degli Studi di Bergamo, by professor Cincinelli Peter in 2026, with given permission.

---

