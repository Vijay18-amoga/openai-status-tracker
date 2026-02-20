from django.apps import AppConfig


class TrackerConfig(AppConfig):
    name = "tracker"

    def ready(self):
        """
        Called once when Django is fully loaded.
        We start the background scheduler here so it kicks off automatically.
        """
        # Guard against double-start (Django calls ready() twice in dev with reloader)
        import os

        if os.environ.get("RUN_MAIN") != "true":
            return
        from tracker.scheduler import start_scheduler

        start_scheduler()
