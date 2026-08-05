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
│   └── reminders.json
│
├── calendar/
│   ├── sheets.py
│   └── parser.py
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
├── utils/
│
├── main.py
│
└── README.md
```

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

Example ensemble configuration:

```json
{
    "Aves": {
        "group_id": "...",
        "enabled": true
    },
    "Octaviation": {
        "group_id": "...",
        "enabled": true
    }
}
```

Example reminder schedule:

```json
[
    7,
    3,
    1
]
```

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
