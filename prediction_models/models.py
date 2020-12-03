from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import re


class PredictionModel(models.Model):
    model_hash_code = models.CharField(max_length=256)

    storage_path = models.CharField(max_length=1064)

    created_at = models.DateTimeField('date created', auto_now_add=True)

    last_updated_at = models.DateTimeField('last update', auto_now=True)

    STATE_CREATED = 'CREATED'
    STATE_ON_TRAIN = 'ON_TRAIN'
    STATE_TRAINED = 'TRAINED'
    STATE_FAILED = 'FAILED'

    PREDICTION_MODEL_STATES = [
        (STATE_CREATED, 'CREATED'),
        (STATE_ON_TRAIN, 'ON TRAIN'),
        (STATE_TRAINED, 'TRAINED'),
        (STATE_FAILED, 'FAILED'),
    ]
    # on train/ trained/ failed
    state = models.CharField(
        max_length=8,
        choices=PREDICTION_MODEL_STATES,
        default=STATE_CREATED,
    )

    def export_model(self):
        # TODO
        pass

    @classmethod
    def list_models_from_fs(cls, models_folder_path):
        """Given a path to models it checks folders and finds valid models"""
        pass

    @classmethod
    def validate_model_folder(cls, model_path):
        """checks if folder contains valid IC model"""
        pass
