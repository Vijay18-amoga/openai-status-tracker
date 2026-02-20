# run_tracker.py
# Standalone script — runs the OpenAI status tracker directly from the terminal
# without needing to start the full Django web server.
#
# Usage:
#   source venv/bin/activate
#   python run_tracker.py

import os
import sys
import time

import django

# Point Django at our settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "status_tracker.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tracker.monitor import check_and_print_new_updates

POLL_INTERVAL_SECONDS = 60

if __name__ == "__main__":
    print("=" * 60)
    print("  OpenAI Status Tracker — Console Mode")
    print(f"  Polling every {POLL_INTERVAL_SECONDS} seconds for new incidents.")
    print("  Press Ctrl+C to stop.")
    print("=" * 60)

    try:
        while True:
            check_and_print_new_updates()
            time.sleep(POLL_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n[Tracker] Stopped by user.")
