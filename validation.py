from financial_schema import FINANCIAL_SCHEMA

def normalize_variable_name(name):
    for key, meta in FINANCIAL_SCHEMA.items():
        if name in meta["aliases"]:
            return meta["canonical"]
    return name


def validate_required_fields(data, required_fields):
    missing = [field for field in required_fields if field not in data or data[field] is None]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    return data
