# saints/apps.py
from django.apps import AppConfig

class SdntsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sdnts'

    def ready(self):
        # Importa las señales cuando la app esté lista
        import sdnts.signals.handlers