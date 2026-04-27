# Corporate Finance Calc

A Streamlit-based calculator for corporate finance, built to support common cash flow and valuation calculations without relying on spreadsheets.

# Future update:
- implementation of data reading to import values from excel

## Features

### Cash Flow
Calculates the main cash flow metrics used in corporate finance:

- **FCCNOGC** — from operating revenues/costs, MOL, or EBIT
- **RO-L** — from operating revenues/costs or MOL
- **FCGC** — from FCCNOGC and ΔCCNO
- **FCID** — from investments and disinvestments
- **FCFR** — from net equity, financial debt, and capital repayment
- **FCRf** — from financial charges and dividends
- **FCU** — from FCGC and FCID
- **Variazione Liquidità** — from FCGC, FCID, FCFR, FCRf
- **FCE** — from FCU, FCFR, FCRf, capital repayment, and dividends

Each section accepts either direct input of the final value or its components. Previously calculated values are automatically carried forward as dependencies.

### NPV
Net Present Value calculation with:
- Variable number of periods
- Per-period cash flows and timing
- Fixed cost per period
- Custom discount rate

## Project Structure
```
Corporate-Finance-Calc/
├── app.py          # Streamlit interface
├── formulas.py     # Pure Python calculation logic
├── LICENSE
├── NOTICE
└── README.md
```
The calculation logic in `formulas.py` is completely decoupled from the interface, making it independently testable.

## Installation
```bash
git clone https://github.com/Liukpro/Corporate-Finance-Calc
cd Corporate-Finance-Calc
pip install -r requirements.txt
streamlit run app.py
```

## Requirements
```
streamlit
numpy
```

## Roadmap
- Bonds Evaluation
- Stock Evaluation (DDM, Gordon Growth Model)
- Depreciation: French and Italian methods
- NPV Comparison between projects
- Portfolio Theory

## License
This project is licensed under the terms specified in the LICENSE file.
