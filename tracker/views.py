from django.http import HttpResponse

from tracker.monitor import seen_updates


def index(request):
    """Shows how many incidents are currently being tracked."""
    count = len(seen_updates)
    html = f"""
    <html>
    <head><title>OpenAI Status Tracker</title></head>
    <body>
        <h2>OpenAI Status Tracker is Running</h2>
        <p>Tracking <strong>{count}</strong> incident(s) so far.</p>
        <p>New updates are printed to the <strong>server console</strong> automatically every 60 seconds.</p>
    </body>
    </html>
    """
    return HttpResponse(html)
