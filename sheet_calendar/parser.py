import re
from datetime import datetime, date
from typing import Dict, List

from models.event import Event

MONTHS = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
    'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
}

_MONTH_HEADER_RE = re.compile(r'^([A-Za-z]+)(?:,?\s*(\d{4}))?$')
_DAY_NUM_RE = re.compile(r'(\d{1,2})')


def parse_rows(rows: List[dict]) -> List[Event]:
    """Legacy parser for the tidy sample CSV (title, start_date, ...)."""
    events = []
    for r in rows:
        title = r.get('title') or r.get('Title')
        date_str = r.get('start_date') or r.get('date')
        start_time = r.get('start_time') or ''
        end_time = r.get('end_time') or ''
        location = r.get('location') or ''
        ensembles = [e.strip() for e in (r.get('ensembles') or '').split(';') if e.strip()]
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d').date()
        except Exception:
            continue
        event = Event(title=title, date=dt, start_time=start_time, end_time=end_time, location=location, ensembles=ensembles)
        events.append(event)
    return events


def _match_month_header(row: List[str]):
    """Return (month_num, year_or_None) if row is a 'July' / 'January, 2027' section header, else None."""
    if not row:
        return None
    first = (row[0] or '').strip()
    if not first:
        return None
    if any((c or '').strip() for c in row[1:]):
        return None
    m = _MONTH_HEADER_RE.match(first)
    if not m:
        return None
    month_name = m.group(1).lower()
    if month_name not in MONTHS:
        return None
    year = int(m.group(2)) if m.group(2) else None
    return (MONTHS[month_name], year)


OCTAVIATION_TRIGGER = 'Octaviation'
OCTAVIATION_COLOR_WORDS = {
    'white': 'Octaviation White',
    'green': 'Octaviation Green',
    'gold': 'Octaviation Gold',
}


def _resolve_octaviation(text_lower: str, matched: set) -> set:
    """'Octaviation' is a virtual trigger, not a real GroupMe group. Calendar titles
    often list colors without repeating "Octaviation"/"Octa" for each one (e.g.
    "Octaviation White, Green, and Gold" or "OctaGold"), so once the trigger has
    matched, look for bare color words anywhere in the title: if any are found,
    only those colors get the reminder; if none are, all three do.
    """
    matched = set(matched)
    if OCTAVIATION_TRIGGER not in matched:
        return matched
    matched.discard(OCTAVIATION_TRIGGER)
    colors = {ensemble for word, ensemble in OCTAVIATION_COLOR_WORDS.items() if word in text_lower}
    matched.update(colors or OCTAVIATION_COLOR_WORDS.values())
    return matched


def match_ensembles(text: str, keyword_map: Dict[str, List[str]]) -> List[str]:
    """Match event text against a {ensemble: [keywords]} map. 'ALL' keywords apply to every ensemble."""
    text_lower = text.lower()
    matched = set()
    for kw in keyword_map.get('ALL', []):
        if kw.lower() in text_lower:
            matched = {k for k in keyword_map if k != 'ALL'}
            return sorted(_resolve_octaviation(text_lower, matched))
    for ensemble, keywords in keyword_map.items():
        if ensemble == 'ALL':
            continue
        for kw in keywords:
            if kw.lower() in text_lower:
                matched.add(ensemble)
                break
    return sorted(_resolve_octaviation(text_lower, matched))


def parse_calendar_grid(rows: List[List[str]], start_year: int, keyword_map: Dict[str, List[str]] = None) -> List[Event]:
    """Parse a raw month-grid calendar export: month header rows followed by
    (day, weekday, event, time, location) rows. Dates have no year printed, so the
    year is tracked from `start_year` and bumped whenever the month number rolls
    backward (e.g. December -> January), or set explicitly by a 'Month, YYYY' header.
    """
    keyword_map = keyword_map or {}
    events = []
    current_month = None
    current_year = start_year
    prev_month_num = None

    for row in rows:
        if not row or not any((c or '').strip() for c in row):
            continue

        header = _match_month_header(row)
        if header:
            month_num, explicit_year = header
            if explicit_year is not None:
                current_year = explicit_year
            elif prev_month_num is not None and month_num < prev_month_num:
                current_year += 1
            current_month = month_num
            prev_month_num = month_num
            continue

        if current_month is None:
            continue

        day_cell = (row[0] or '').strip()
        day_match = _DAY_NUM_RE.search(day_cell)
        if not day_match:
            continue

        title = (row[2] if len(row) > 2 else '').strip()
        if not title:
            continue

        try:
            event_date = date(current_year, current_month, int(day_match.group(1)))
        except ValueError:
            continue

        time_info = (row[3] if len(row) > 3 else '').strip()
        location = (row[4] if len(row) > 4 else '').strip()
        ensembles = match_ensembles(title, keyword_map)

        events.append(Event(
            title=title,
            date=event_date,
            start_time=time_info,
            end_time='',
            location=location,
            ensembles=ensembles,
        ))

    return events
