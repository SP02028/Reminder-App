from datetime import datetime
from typing import List
from models.event import Event

def parse_rows(rows: List[dict]) -> List[Event]:
    events = []
    for r in rows:
        title = r.get('title') or r.get('Title')
        date_str = r.get('start_date') or r.get('date')
        start_time = r.get('start_time') or ''
        end_time = r.get('end_time') or ''
        location = r.get('location') or ''
        ensembles = [e.strip() for e in (r.get('ensembles') or '').split(';') if e.strip()]
        # parse date
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            continue
        event = Event(title=title, date=dt, start_time=start_time, end_time=end_time, location=location, ensembles=ensembles)
        events.append(event)
    return events
