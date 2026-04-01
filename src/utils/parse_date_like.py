from datetime import datetime
from utils.safe_str import safe_str 

def parse_date_like(value, default=None):
    if value is None or value == "":
        return default or datetime.now().date()
    if isinstance(value, datetime):
        return value.date()
    if hasattr(value, "date"):
        try:
            return value.date()
        except Exception:
            pass
    text = safe_str(value)
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"]:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return default or datetime.now().date()