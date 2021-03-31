from django.apps import AppConfig


class AcademicConfig(AppConfig):
    name = 'api.academic'

    def ready(self):
        from .signals import create_departament_and_plans
