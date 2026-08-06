import json
from pathlib import Path
from typing import Dict

def send_message(group_id: str, message: str, storage_path: str):
    # Stub: instead of sending to GroupMe, record message locally.
    record = {"group_id": group_id, "message": message}
    p = Path(storage_path)
    data = []
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding='utf-8') or '[]')
        except Exception:
            data = []
    data.append(record)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(f"[groupme stub] Would send to {group_id}: {message}")
