# Choir Reminder Bot

An automated reminder system that reads events from a Google Sheets calendar and sends scheduled reminders to the appropriate GroupMe chats.

## Overview

Managing communication across multiple ensembles can be repetitive and time-consuming. This project automates that process by syncing with the choir calendar, determining which groups are affected by each event, generating reminder messages, and sending them at configurable intervals.

Rather than replacing directors or student leaders, the bot is designed to reduce repetitive work while still allowing manual oversight when needed.

## Goals

* Automatically read events from a shared Google Sheet
* Identify which ensembles each event applies to
* Generate clear reminder messages
* Send reminders to the appropriate GroupMe chats
* Allow optional manual review before messages are sent
* Keep the system configurable for future years

## Features (MVP)

* Google Sheets integration
* Automatic event parsing
* Ensemble filtering
* Scheduled reminders (1 week, 3 days, 1 day, etc.)
* GroupMe messaging
* Duplicate reminder prevention
* Configurable reminder schedule

## Planned Features

* Admin approval workflow
* Reminder preview
* Custom reminder templates
* Web dashboard
* Multiple organization support
* Discord/Slack support
* Email notifications
* Analytics and reminder history

## Project Structure

```text
groupme-reminder-bot/
│
├── config/
│   ├── settings.py
│   ├── ensembles.json
│   ├── ensemble_keywords.json
│   └── reminders.json
│
├── sheet_calendar/
│   ├── sheets.py
│   ├── parser.py
│   └── choral_calendar_2026_2027.csv
│
├── models/
│   ├── event.py
│   └── reminder.py
│
├── scheduler/
│   └── scheduler.py
│
├── messaging/
│   └── groupme.py
│
├── storage/
│   └── sent_reminders.json
│
├── .env.example
├── requirements.txt
├── main.py
│
└── README.md
```

> Note: the calendar package is named `sheet_calendar`, not `calendar` — a package
> literally named `calendar` shadows Python's built-in `calendar` module (used
> internally by `requests` and others) for anything run from this project root.

`scheduler/` is not built yet — `main.py` currently runs once per invocation rather
than as a recurring job. `sheet_calendar/sheets.py` currently reads a CSV export of
the calendar rather than calling the Google Sheets API directly.

## Workflow

```
Google Sheet
      │
      ▼
Read calendar
      │
      ▼
Parse events
      │
      ▼
Determine affected ensembles
      │
      ▼
Generate reminder
      │
      ▼
(Optional) Admin review
      │
      ▼
Send to GroupMe
      │
      ▼
Record reminder as sent
```

## Example Reminder

> 🎶 **Choir Reminder**
>
> **Aves Rehearsal**
>
> 📅 Wednesday, August 20
>
> 🕒 3:00–5:00 PM
>
> 📍 Choir Room
>
> Please bring your folder and water.

## Technologies

* Python
* Google Sheets API
* GroupMe API
* APScheduler (or cron)
* JSON configuration

## Configuration

The bot is designed to be configurable without changing code.

### Ensembles and GroupMe bots (`config/ensembles.json`)

Each ensemble maps to the name of an environment variable holding its GroupMe bot ID
(create one bot per group at https://dev.groupme.com/bots):

```json
{
    "Select": {
        "bot_env_var": "GROUPME_BOT_ID_SELECT",
        "enabled": true
    },
    "Octaviation White": {
        "bot_env_var": "GROUPME_BOT_ID_OCTAVIATION_WHITE",
        "enabled": true
    }
}
```

Set the actual bot IDs in a `.env` file (copy `.env.example`, never commit `.env`).
An ensemble whose bot ID is unset falls back to a local stub — it prints and records
the reminder instead of posting to GroupMe, so the pipeline stays runnable while
bots are being set up.

### Ensemble keyword matching (`config/ensemble_keywords.json`)

The calendar export has no "ensembles" column, so ensembles are inferred by matching
keywords against each event's title (case-insensitive substring match):

```json
{
    "ALL": ["all choirs", "all ensembles", "all-choral"],
    "Select": ["select"],
    "Octaviation": ["octaviation", "octa"]
}
```

Any keyword under `"ALL"` matches every configured ensemble. This list needs regular
upkeep — new abbreviations, nicknames, or one-off event names in the calendar won't
match anything until a keyword for them is added here.

`Octaviation` is a special case: it isn't a real GroupMe group, just a trigger
(matched here, then resolved in `sheet_calendar/parser.py`). Calendar titles list
colors inconsistently ("Octaviation White, Green, and Gold", "OctaGold", "Green and
Gold"), so once "Octaviation"/"Octa" is found anywhere in the title, the parser
looks for the bare words "white"/"green"/"gold" in that same title: any colors it
finds get only that color's group messaged; if it finds none, all three
(White/Green/Gold) get it.

### Reminder schedule (`config/reminders.json`)

```json
[
    7,
    3,
    1
]
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in GroupMe bot IDs as they're created
python main.py
```

`config/settings.py` currently points at `sheet_calendar/choral_calendar_2026_2027.csv`
(a manual CSV export of the calendar) and treats every reminder as due immediately
(`demo_send_immediately: True`) so a run is easy to sanity-check. Turn that off and
wire a real recurring trigger (cron, Task Scheduler, or the not-yet-built
`scheduler/`) once real dates matter.

## Future Improvements

* Natural-language reminder generation
* Google Calendar integration
* Attendance tracking
* Automatic conflict detection
* Push notifications
* Mobile-friendly admin interface
* Support for additional student organizations

## Motivation

Large student organizations often rely on volunteers to manually remind members about rehearsals, performances, deadlines, and events. This project automates that repetitive process while keeping student leaders in control of the final communication.

Although originally built for a high school choir program, the underlying reminder system is designed to be adaptable to any organization that manages events through a shared spreadsheet.

## License

MIT License
