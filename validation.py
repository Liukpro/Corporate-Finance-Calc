import pandas as pd


REQUIRED_COLUMNS = [
    "ric_op_mon",
    "cost_op_mon",
    "amortisat",
    "tax",
    "patrimonio_netto",
    "debiti_finanz",
    "liquidity",
    "oneri_finanz",
    "ccno1",
    "ccno2",
    "acquisition_1",
    "acquisition_2",
    "valore_stor",
    "ammo_ti",
    "n_ammo_ti",
    "plus",
    "minus",
    "quota_rimbors_capital",
    "dividendi",
    "fc",
    "cost",
    "k",
    "t",
]


###########################################################################

def check_required_fields(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    return df


###########################################################################

def enforce_numeric_schema(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


###########################################################################

def normalize_units(df: pd.DataFrame, scale: float = 1.0) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols] * scale
    return df


###########################################################################

SYNONYM_MAP = {
    "EBIT": "rol",
    "ROL": "rol",
    "MOL": "mol",
    "EBITDA": "mol",
}


def map_synonyms(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={k.lower(): v for k, v in SYNONYM_MAP.items() if k.lower() in df.columns})
    return df


###########################################################################

def sanity_checks(df: pd.DataFrame) -> pd.DataFrame:
    if (df["patrimonio_netto"] < 0).any():
        raise ValueError("Invalid negative equity detected")

    if (df["ric_op_mon"] < 0).any():
        raise ValueError("Negative revenue detected")

    if (df["ccno1"].isna().any() or df["ccno2"].isna().any()):
        raise ValueError("Missing CCNO data")

    return df


###########################################################################

def validate_pipeline(df: pd.DataFrame, scale: float = 1.0) -> pd.DataFrame:
    df = check_required_fields(df)
    df = enforce_numeric_schema(df)
    df = map_synonyms(df)
    df = normalize_units(df, scale=scale)
    df = sanity_checks(df)
    return df
