from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class Reminder:
    event_title: str
    event_date: date
    days_before: int
    ensemble: str
    scheduled_for: datetime
