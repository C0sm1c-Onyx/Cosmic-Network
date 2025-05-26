from django.apps import AppConfig


class InteractionCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interaction_core'

    def ready(self):
        import interaction_core.signals