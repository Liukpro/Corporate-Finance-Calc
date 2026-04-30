import pandas as pd


###########################################################################
#input

def load_excel(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    return df


###########################################################################
#cleaning

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures numeric stability for DAG computations.
    """

    # force numeric where possible
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = pd.to_numeric(df[col], errors="ignore")

    # fill missing numeric values with 0 (safe default for finance DAGs)
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    return df


###########################################################################
#dag entrypoint

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares all required inputs for your DAG.
    This is the ONLY place where raw columns become financial structure.
    """

    # Core profitability
    df["mol"] = df["ric_op_mon"] - df["cost_op_mon"]
    df["rol"] = df["mol"] - df["amortisat"]

    # FCCNOGC
    df["fccnogc_from_revenue"] = df["ric_op_mon"] - df["cost_op_mon"] - df["tax"]
    df["fccnogc_from_mol"] = df["mol"] - df["tax"]
    df["fccnogc_from_rol"] = df["rol"] - df["tax"] + df["amortisat"]

    # ROS
    df["ros"] = df["rol"] / df["ric_op_mon"]

    # CIN / ROI
    df["cin"] = df["patrimonio_netto"] + df["debiti_finanz"] - df["liquidity"]
    df["roi"] = df["rol"] / df["cin"]

    # Net profit / ROE
    df["utile_netto"] = df["rol"] - df["oneri_finanz"] - df["tax"]
    df["roe"] = df["utile_netto"] / df["patrimonio_netto"]

    # Working capital flows
    df["var_ccno"] = df["ccno2"] - df["ccno1"]
    df["fcgc"] = df["fccnogc_from_mol"] - df["var_ccno"]

    # Investments
    df["inv"] = df["acquisition_2"] - df["acquisition_1"]
    df["vnc"] = df["valore_stor"] - (df["ammo_ti"] * df["n_ammo_ti"])
    df["dis_from_vnc"] = df["vnc"] + df["plus"] - df["minus"]
    df["fcid"] = df["dis_from_vnc"] - df["inv"]

    # Financing
    df["fcfr"] = df["patrimonio_netto"] + df["debiti_finanz"] - df["quota_rimbors_capital"]

    # Financial remuneration
    df["fcrf"] = -df["oneri_finanziari"] - df["dividendi"]

    # Cash flow aggregation
    df["var_liquidity"] = df["fcgc"] + df["fcid"] + df["fcfr"] + df["fcrf"]

    df["fcu"] = df["fcgc"] + df["fcid"]
    df["fce"] = df["fcu"] + df["fcfr"] - df["quota_rimbors_capital"] + df["fcrf"] - df["dividendi"]

    # NPV support
    df["fc_net"] = df["fc"] - df["cost"]

    df["df"] = (1 + df["k"]) ** df["t"]
    df["pv"] = df["fc_net"] / df["df"]

    return df


###########################################################################


def dataframe_to_dict(df: pd.DataFrame):
    return df.to_dict(orient="records")


###########################################################################


def run_data_pipeline(file_path: str):
    df = load_excel(file_path)
    df = normalize_dataframe(df)
    df = build_features(df)
    return df
