from django.apps import AppConfig

class FormConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'form'
    def ready(self):
        from .signals import connect_lab_signals
        connect_lab_signals()

