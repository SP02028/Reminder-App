import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from config.settings import SETTINGS
from sheet_calendar.sheets import read_calendar_grid
from sheet_calendar.parser import parse_calendar_grid
from messaging.groupme import send_message, load_sent_keys


def load_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def format_reminder(event, days_before):
    date_str = event.date.strftime('%A, %B %d')
    lines = ["🎶 **Choir Reminder**", "", f"**{event.title}**", "", f"📅 {date_str}"]
    if event.start_time:
        lines += ["", f"🕒 {event.start_time}"]
    if event.location:
        lines += ["", f"📍 {event.location}"]
    when = "today!" if days_before == 0 else f"{days_before} day{'s' if days_before != 1 else ''} away"
    lines += ["", f"({when})"]
    return "\n\n".join(lines)


def reminder_key(event, ensemble, days_before):
    return f"{event.date.isoformat()}|{ensemble}|{days_before}|{event.title}"


def main():
    settings = SETTINGS
    rows = read_calendar_grid(settings['sheet_csv'])
    keyword_map = load_json(settings['ensemble_keywords_file']) or {}
    events = parse_calendar_grid(rows, settings['calendar_start_year'], keyword_map)

    ensembles_cfg = load_json(settings['ensembles_file']) or {}
    reminders_schedule = load_json(settings['reminders_file']) or [7, 3, 1]

    storage = settings['storage_file']
    already_sent = load_sent_keys(storage)

    now = datetime.now()
    sent_count = 0
    skipped_duplicates = 0

    horizon_days = max(reminders_schedule) if reminders_schedule else 0
    unmatched = [
        ev for ev in events
        if not ev.ensembles and now.date() <= ev.date <= now.date() + timedelta(days=horizon_days)
    ]
    for ev in unmatched:
        print(f"[warning] no ensemble matched for upcoming event on {ev.date}: {ev.title!r} "
              f"-- add a keyword to config/ensemble_keywords.json or it won't get a reminder.")

    for ev in events:
        if ev.date < now.date():
            continue

        for ensemble in ev.ensembles:
            cfg = ensembles_cfg.get(ensemble, {})
            if not cfg.get('enabled', True):
                continue
            bot_id = os.environ.get(cfg.get('bot_env_var', ''))

            for days in reminders_schedule:
                key = reminder_key(ev, ensemble, days)
                if key in already_sent:
                    skipped_duplicates += 1
                    continue

                scheduled_for = datetime.combine(ev.date, datetime.min.time()) - timedelta(days=days)
                if not settings.get('demo_send_immediately') and scheduled_for > now:
                    continue

                message = format_reminder(ev, days)
                send_message(ensemble, message, storage, key=key, bot_id=bot_id)
                already_sent.add(key)
                sent_count += 1

    print(f"Sent {sent_count} reminders, skipped {skipped_duplicates} duplicates, "
          f"{len(unmatched)} unmatched upcoming events (demo mode={settings.get('demo_send_immediately')}).")


if __name__ == '__main__':
    main()
