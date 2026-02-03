from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'
    
    def ready(self):
        # Import signal handlers to ensure automatic notifications are wired
        # when the app registry is ready.
        try:
            from . import signals  # noqa: F401
        except Exception:
            # Don't let signal import errors break management commands; log to stdout
            import sys
            print('Warning: could not import library.signals', file=sys.stderr)
