import pandas as pd

def load_excel(file_path):
    df = pd.read_excel(file_path)
    return df


def dataframe_to_dict(df):
    data = df.to_dict(orient="records")
    return data
