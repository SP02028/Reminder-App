import json
from datetime import datetime, timezone
from pathlib import Path

import requests

GROUPME_POST_URL = "https://api.groupme.com/v3/bots/post"


def _load_storage(storage_path: str):
    p = Path(storage_path)
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding='utf-8') or '[]')
    except Exception:
        return []


def _save_storage(storage_path: str, data):
    p = Path(storage_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2), encoding='utf-8')


def load_sent_keys(storage_path: str) -> set:
    """Keys of reminders already recorded as sent, for duplicate prevention."""
    return {record.get('key') for record in _load_storage(storage_path) if record.get('key')}


def send_message(ensemble: str, message: str, storage_path: str, key: str = None, bot_id: str = None):
    """Send a reminder to GroupMe via a bot, and record it in storage_path either way.

    If bot_id is missing, falls back to a local stub (prints + records only) so the
    pipeline stays runnable before real GroupMe bots are configured.
    """
    record = {
        "key": key,
        "ensemble": ensemble,
        "message": message,
        "sent_at": datetime.now(timezone.utc).isoformat(),
    }

    if bot_id:
        try:
            resp = requests.post(GROUPME_POST_URL, json={"bot_id": bot_id, "text": message}, timeout=10)
            record["delivery"] = "sent" if resp.status_code == 202 else f"error:http_{resp.status_code}"
        except requests.RequestException as exc:
            record["delivery"] = f"error:{exc}"
    else:
        record["delivery"] = "stub (no bot_id configured)"
        print(f"[groupme stub] Would send to {ensemble}: {message}")

    data = _load_storage(storage_path)
    data.append(record)
    _save_storage(storage_path, data)
