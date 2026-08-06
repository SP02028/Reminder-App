from datetime import datetime, timedelta
import json
from pathlib import Path

from config.settings import SETTINGS
from calendar.sheets import read_sheet_csv
from calendar.parser import parse_rows
from messaging.groupme import send_message


def load_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def format_reminder(event, days_before):
    date_str = event.date.strftime('%A, %B %d')
    lines = ["🎶 **Choir Reminder**", "", f"**{event.title}**", "", f"📅 {date_str}", "", f"📍 {event.location}", "", "Please bring your folder and water."]
    return "\n\n".join(lines)


def main():
    settings = SETTINGS
    rows = read_sheet_csv(settings['sheet_csv'])
    events = parse_rows(rows)
    ensembles_cfg = load_json(settings['ensembles_file']) or {}
    reminders_schedule = load_json(settings['reminders_file']) or [7,3,1]

    now = datetime.now()
    to_send = []
    for ev in events:
        for ensemble in ev.ensembles:
            cfg = ensembles_cfg.get(ensemble, {})
            if not cfg.get('enabled', True):
                continue
            group_id = cfg.get('group_id', f'group_{ensemble}')
            for days in reminders_schedule:
                scheduled_for = datetime.combine(ev.date, datetime.min.time()) - timedelta(days=days)
                # Demo mode: send immediately but note schedule
                if settings.get('demo_send_immediately'):
                    to_send.append((group_id, format_reminder(ev, days), scheduled_for))
                else:
                    if scheduled_for <= now:
                        to_send.append((group_id, format_reminder(ev, days), scheduled_for))

    storage = settings['storage_file']
    for group_id, message, scheduled_for in to_send:
        # record and send via stub
        send_message(group_id, message + f"\n\n(Originally scheduled for {scheduled_for.isoformat()})", storage)

    print(f"Sent {len(to_send)} reminders (demo mode={settings.get('demo_send_immediately')}).")


if __name__ == '__main__':
    main()
