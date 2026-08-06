import json
from pathlib import Path

ROOT = Path(__file__).parent.parent

def load_settings():
    # Minimal settings for demo purposes
    return {
        "sheet_csv": str(ROOT / "calendar" / "sample_events.csv"),
        "ensembles_file": str(ROOT / "config" / "ensembles.json"),
        "reminders_file": str(ROOT / "config" / "reminders.json"),
        "storage_file": str(ROOT / "storage" / "sent_reminders.json"),
        "demo_send_immediately": True
    }

SETTINGS = load_settings()
