# 🟢 OpenAI Status Tracker

A lightweight Django app that **automatically monitors the [OpenAI Status Page](https://status.openai.com)** and prints new incidents, outages, or degradation events directly to your console — without manual refreshing.

---

## 📋 Table of Contents

- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Tracker](#running-the-tracker)
  - [Option 1 — Console Mode (Recommended)](#option-1--console-mode-recommended)
  - [Option 2 — Django Server Mode](#option-2--django-server-mode)
- [Example Output](#example-output)
- [Configuration](#configuration)
- [Architecture Explained](#architecture-explained)

---

## How It Works

1. Every **60 seconds** the app calls the OpenAI Statuspage.io **public JSON API**:

   ```
   GET https://status.openai.com/api/v2/incidents.json
   ```

2. It compares each incident's latest update ID against a local `seen_updates` dictionary.
3. **Only new or changed updates** trigger a console print — this is the event-based mechanism.
4. Nothing is printed if there are no changes since the last check.

---

## Project Structure

```
status_tracker/
│
├── run_tracker.py            ← ✅ Standalone console runner (start here)
├── manage.py                 ← Django management CLI
├── db.sqlite3                ← SQLite DB (auto-created by Django)
│
├── status_tracker/           ← Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── tracker/                  ← Main app
    ├── fetcher.py            ← Calls the OpenAI status JSON API
    ├── monitor.py            ← Compares updates, prints new ones
    ├── scheduler.py          ← Background thread, polls every 60s
    ├── apps.py               ← Auto-starts scheduler on Django boot
    ├── views.py              ← Simple browser status page
    └── urls.py               ← URL routing
```

---

## Prerequisites

- **Python 3.10+** installed
- **pip** available
- **macOS / Linux / Windows** (all supported)
- Internet access to reach `status.openai.com`

Check your Python version:

```bash
python3 --version
```

---

## Installation

### Step 1 — Clone or download the project

```bash
git clone <your-repo-url>
cd status_tracker
```

> If you downloaded a ZIP, extract it and `cd` into the folder.

---

### Step 2 — Create a virtual environment

```bash
python3 -m venv venv
```

---

### Step 3 — Activate the virtual environment

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your terminal prompt.

---

### Step 4 — Install dependencies

```bash
pip install django requests
```

---

### Step 5 — Run database migrations

```bash
python manage.py migrate
```

This creates the `db.sqlite3` file needed by Django.

---

## Running the Tracker

### Option 1 — Console Mode (Recommended)

This is the **simplest way** to run the tracker. It requires no browser, no web server — just your terminal.

```bash
python run_tracker.py
```

**What happens:**

- Immediately fetches and prints all current OpenAI incidents on startup.
- Then waits 60 seconds and checks again.
- Only prints something when a **new** incident or update is detected.
- Press `Ctrl+C` to stop.

---

### Option 2 — Django Server Mode

This runs the full Django web server. The background scheduler starts automatically alongside it.

```bash
python manage.py runserver
```

**What happens:**

- The background thread starts and begins polling every 60 seconds.
- New incidents are printed to the **server console** (same terminal window).
- Visit `http://127.0.0.1:8000/` in your browser to see a simple status page showing how many incidents are being tracked.

---

## Example Output

```
============================================================
  OpenAI Status Tracker — Console Mode
  Polling every 60 seconds for new incidents.
  Press Ctrl+C to stop.
============================================================

[2025-11-03 14:32:00] Incident : Elevated error rates for ChatGPT and Platform users
            Product  : ChatGPT, OpenAI API
            Impact   : Minor  |  State: Investigating
            Status   : We are investigating elevated error rates affecting ChatGPT and API users.
------------------------------------------------------------

[2025-11-03 13:10:00] Incident : High errors with image generation
            Product  : DALL·E
            Impact   : Major  |  State: Identified
            Status   : The issue has been identified and a fix is being implemented.
------------------------------------------------------------

[2025-11-03 15:00:00] No new updates detected.
```

---

## Configuration

To change the polling interval, open `tracker/scheduler.py` and update:

```python
POLL_INTERVAL_SECONDS = 60   # change to any number of seconds
```

The same variable exists in `run_tracker.py` for console mode:

```python
POLL_INTERVAL_SECONDS = 60
```

---

## Architecture Explained

| File | Role |
|---|---|
| `fetcher.py` | Makes a single `GET` request to the Statuspage.io JSON API and returns the raw incident list |
| `monitor.py` | Maintains a `seen_updates` dict (`incident_id → update_id`). Only triggers output when a new `update_id` is found — the "event-based" logic |
| `scheduler.py` | Runs a **daemon background thread** that calls `monitor` every N seconds — non-blocking, zero extra dependencies |
| `apps.py` | Uses Django's `AppConfig.ready()` hook to auto-start the scheduler exactly once when the server boots |
| `run_tracker.py` | Standalone entry point — skips the web server entirely, runs the same polling loop in the foreground |

### Why this scales to 100+ status pages

- Each status page just needs its own entry in `seen_updates`.
- No database writes, no file I/O — just an in-memory dict comparison.
- The daemon thread approach means you can add more pages without adding more threads — just loop through a list of page URLs in `fetcher.py`.

---

## Stopping the Tracker

- **Console mode:** Press `Ctrl+C`
- **Django server:** Press `Ctrl+C` in the terminal running `runserver`
