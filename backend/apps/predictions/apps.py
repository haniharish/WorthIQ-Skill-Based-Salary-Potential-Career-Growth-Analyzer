from django.apps import AppConfig

class PredictionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.predictions'
    verbose_name = 'Salary Predictions'

    def ready(self):
        # Warm up ML models in background or pre-check
        pass
