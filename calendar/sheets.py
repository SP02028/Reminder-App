import csv
from pathlib import Path
from typing import List, Dict

def read_sheet_csv(path: str) -> List[Dict[str, str]]:
    p = Path(path)
    if not p.exists():
        return []
    with p.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
