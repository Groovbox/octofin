from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

class ConfigConfig(AppConfig):
    name = 'config'

    def ready(self):
        try:
            from .settings_loader import load_and_sync_settings
            load_and_sync_settings()
        except (OperationalError, ProgrammingError):
            # Table doesn't exist yet; skip loading
            pass
