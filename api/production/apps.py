from django.apps import AppConfig


class ProductionConfig(AppConfig):
    name = 'api.production'

    def ready(self):
        from .signals import create_types_report
