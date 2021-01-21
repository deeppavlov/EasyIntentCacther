from django.apps import AppConfig
from constance.apps import ConstanceConfig


class PredictionModelsConfig(AppConfig):
    name = 'prediction_models'


class IntentCactherConstance(ConstanceConfig):
    verbose_name = "Easy Intent Catcher Configuration"