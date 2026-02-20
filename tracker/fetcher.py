# tracker/fetcher.py
# Fetches incident data from the OpenAI Status Page (Statuspage.io JSON API)

import requests

# OpenAI uses Statuspage.io — this is the public JSON API endpoint
OPENAI_STATUS_API = "https://status.openai.com/api/v2/incidents.json"


def fetch_incidents():
    """
    Fetches all current and recent incidents from OpenAI status page.
    Returns a list of incident dicts, or empty list on failure.
    """
    try:
        response = requests.get(OPENAI_STATUS_API, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("incidents", [])
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch status page: {e}")
        return []
