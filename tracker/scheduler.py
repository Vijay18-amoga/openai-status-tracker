# tracker/scheduler.py
# Runs the monitor check on a fixed interval using a background thread.
# Using threading keeps things simple — no extra dependencies needed.

import threading
import time

from tracker.monitor import check_and_print_new_updates

# How often (in seconds) to poll the status page
POLL_INTERVAL_SECONDS = 60


def _run_loop():
    """Internal loop: check for updates, then sleep, then repeat."""
    print(f"[Scheduler] Started. Checking every {POLL_INTERVAL_SECONDS}s for new OpenAI incidents...")
    print("=" * 60)
    while True:
        check_and_print_new_updates()
        time.sleep(POLL_INTERVAL_SECONDS)


def start_scheduler():
    """
    Launch the polling loop in a daemon background thread so it runs
    alongside Django without blocking the server.
    (Daemon=True means the thread stops automatically when the main process exits.)
    """
    thread = threading.Thread(target=_run_loop, daemon=True, name="StatusTrackerThread")
    thread.start()
