# Corporate Finance Engine — System Roadmap (Architecture v2)

**Demo on Streamlit:** https://corporate-finance-calc.streamlit.app/

---

**License** 
Please read License files

---

## Vision

Build a deterministic financial analysis engine that transforms raw Excel financial statements into structured, explainable outputs through a multi-layer data pipeline.

The system is designed for:
- financial analysis automation (consulting / audit / advisory use cases)
- full traceability of calculations
- reproducible valuation and ratio computation
- API-first architecture

---

# Core Architecture Principle

The system is strictly layered.

Each layer has:
- one responsibility
- one file
- no overlap of logic

All financial variables are defined once and shared across all layers through a unified schema.

Excel Input
↓
Data Layer (parsing)
↓
Validation / Normalization Layer
↓
Financial Schema (shared definitions)
↓
Multi-path DAG (possible computations)
↓
Resolver (decision engine)
↓
API Layer (output + explanations)

---

# 1. Data Layer (`data_layer.py`)

## Objective
Convert raw Excel files into structured data.

## Responsibilities
- parse Excel files into DataFrame / dict
- enforce correct data types
- standardize column structure
- convert raw values into machine-readable format
- explicitly mark missing values (None / NaN)

## Constraints
- no financial interpretation
- no semantic mapping
- no assumptions about meaning of variables

## Output
Structured but unvalidated dataset

---

# 2. Validation / Normalization Layer (`validation.py`)

## Objective
Ensure data is consistent, complete, and semantically aligned.

## Responsibilities
- check required fields completeness
- detect structural inconsistencies
- normalize units (thousands, millions, etc.)
- map synonyms to standard schema:
  - EBIT, ROL → EBIT
  - MOL → EBITDA
- validate logical constraints (sanity checks)

## Constraints
- no calculation logic
- no formula execution
- no path selection

## Output
Clean, standardized dataset aligned with financial schema

---

# 3. Financial Schema (`financial_schema.py`)

## Objective
Single source of truth for all financial variables.

## Responsibilities
- define all financial variables (EBIT, EBITDA, FCCNOGC, etc.)
- define naming conventions
- define relationships at conceptual level (not computation)
- ensure consistency across DAG and resolver

## Constraints
- no computation
- no data handling
- no logic execution

## Output
Shared reference model used by all system layers

---

# 4. Multi-path DAG (`financial_dag.py`)

## Objective
Define all possible computation paths for each financial variable.

## Structure
- nodes = financial variables
- edges = alternative formulas

## Responsibilities
- define multiple valid computation routes
- represent financial relationships as a graph
- store all alternative derivations

## Constraints
- no decision making
- no data validation
- no fallback logic execution

## Output
Complete dependency graph of financial variables

---

# 5. Resolver Engine (`resolver.py`)

## Objective
Select the optimal computation path for each variable.

## Responsibilities
- check available input variables
- evaluate possible DAG paths
- apply deterministic selection rules
- choose single valid computation route per variable
- handle controlled fallback logic

## Constraints
- no data cleaning
- no schema definition
- no formula definition

## Output
Resolved execution plan (selected paths only)

---

# 6. API Layer (`api.py`)

## Objective
Expose computed financial results in structured format.

## Responsibilities
- execute resolved computation plan
- return final values
- provide computation traceability
- generate explanation metadata:
  - method used
  - computation path
  - missing inputs (if any)
- format output for external consumption (JSON / REST API)

---

# Dependency Rules (Strict)

- data_layer → validation
- validation → schema reference only
- dag → schema reference only
- resolver → dag + schema + validated data
- api → resolver output only

No circular dependencies allowed.

---

# Critical Design Constraint

The system is built around a single unified financial schema.

All layers must:
- use identical variable naming
- reference the same definitions
- avoid local reinterpretation of financial concepts

---

# Key Separation of Concerns

## Validation Layer vs Resolver Layer

Validation:
- ensures data correctness
- fixes structure and meaning
- prepares dataset

Resolver:
- selects computation paths
- decides how variables are derived
- operates on already clean data

These two responsibilities must never overlap.

---

# System Output Philosophy

All outputs must be:
- deterministic
- explainable
- traceable
- reproducible

No hidden logic inside formulas or ad-hoc fallback inside computations.

---

# Final Target

The system must function as a financial computation engine where:

- Excel is only an input format
- Python is the deterministic computation layer
- API is the final interface layer
- all financial logic is graph-based and fully traceable

---

# Global Pipeline
