import csv
from pathlib import Path
from typing import Dict, List


def read_sheet_csv(path: str) -> List[Dict[str, str]]:
    """Read a tidy CSV with a header row (title, start_date, ...). Used by the sample fixture."""
    p = Path(path)
    if not p.exists():
        return []
    with p.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def read_calendar_grid(path: str) -> List[List[str]]:
    """Read a raw month-grid export (e.g. a Google Sheets CSV export) with no header row."""
    p = Path(path)
    if not p.exists():
        return []
    with p.open(newline='', encoding='utf-8') as f:
        return [row for row in csv.reader(f)]
