def safe_str(value) -> str:
    if value is None:
        return ""
    return str(value).strip()