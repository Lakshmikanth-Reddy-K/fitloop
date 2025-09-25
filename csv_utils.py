import csv
import io
from typing import Dict, List

def read_csv_from_string(csv_content: str) -> List[Dict]:
    """Read CSV content from string and return list of dictionaries"""
    try:
        reader = csv.DictReader(io.StringIO(csv_content))
        return list(reader)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def safe_float(value: str, default: float = 0.0) -> float:
    """Safely convert string to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value: str, default: int = 0) -> int:
    """Safely convert string to int"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default