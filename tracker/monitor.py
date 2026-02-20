# tracker/monitor.py
# Detects new or updated incidents and prints them to the console.

from datetime import datetime

from tracker.fetcher import fetch_incidents

# Keeps track of incident_id -> latest update_id already printed
# This is the "event-based" mechanism: only act when something new appears
seen_updates = {}


def parse_affected_components(incident):
    """Return a comma-separated list of affected product/component names."""
    components = incident.get("components", [])
    if components:
        return ", ".join(c["name"] for c in components)
    # Fall back to the incident name itself
    return incident.get("name", "Unknown Service")


def check_and_print_new_updates():
    """
    Fetch all incidents, compare against already-seen update IDs,
    and print only the NEW ones. Safe to call repeatedly.
    """
    incidents = fetch_incidents()
    found_new = False

    for incident in incidents:
        incident_id = incident.get("id")
        updates = incident.get("incident_updates", [])

        if not updates:
            continue

        # Statuspage.io always returns the latest update first
        latest_update = updates[0]
        update_id = latest_update.get("id")

        # Skip if we have already printed this exact update
        if seen_updates.get(incident_id) == update_id:
            continue

        # Mark as seen so we don't print it again
        seen_updates[incident_id] = update_id
        found_new = True

        product = parse_affected_components(incident)
        incident_name = incident.get("name", "Unknown Incident")
        impact = incident.get("impact", "unknown").capitalize()
        incident_status = incident.get("status", "unknown").replace("_", " ").capitalize()

        # Use the update body if available, otherwise fall back to incident status
        status_body = latest_update.get("body", "").strip()
        if not status_body:
            status_body = f"Incident marked as: {incident_status}"

        raw_time = latest_update.get("created_at", "")

        # Convert ISO timestamp to a readable format
        try:
            dt = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            timestamp = raw_time

        print(f"\n[{timestamp}] Incident : {incident_name}")
        print(f"            Product  : {product}")
        print(f"            Impact   : {impact}  |  State: {incident_status}")
        print(f"            Status   : {status_body}")
        print("-" * 60)

    if not found_new:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] No new updates detected.")
