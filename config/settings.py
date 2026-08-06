import json
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT = Path(__file__).parent.parent


def load_settings():
    return {
        "sheet_csv": str(ROOT / "sheet_calendar" / "choral_calendar_2026_2027.csv"),
        "calendar_start_year": 2026,
        "ensembles_file": str(ROOT / "config" / "ensembles.json"),
        "ensemble_keywords_file": str(ROOT / "config" / "ensemble_keywords.json"),
        "reminders_file": str(ROOT / "config" / "reminders.json"),
        "storage_file": str(ROOT / "storage" / "sent_reminders.json"),
        "demo_send_immediately": False,
    }


SETTINGS = load_settings()
