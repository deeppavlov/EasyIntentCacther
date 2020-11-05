from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import re
# Create your models here.
class Intent(models.Model):
    # name of the intent
    intent_name = models.CharField(max_length=2000)

    # minimal precision for intent element
    min_precision = models.FloatField(default=0.9)

    # phrases
    # reg_phrases
    # punctuation

    # def __repr__(self):
    #     return f"{self.input_data}/{self.golden_label}"
    #
    def __str__(self):
        return f"Intent: <{self.intent_name}>"

    def validate(self):
        # compare tokenized lengths
        pass

    def generate_json_repr(self):
        pass


# TODO support many2many pharse-intents relations and intentless phrases?
class PhraseExpression(models.Model):
    parent_intent = models.ForeignKey(
        Intent,
        on_delete=models.CASCADE,
        related_name="phrases"
    )

    text = models.CharField(max_length=2000)

    def clean(self):
        # print("Clean validation is called")
        if self.text:
            try:
                re.compile(self.text)
                # print("regexp is valid")
            except re.error:
                raise ValidationError(f"WARNING: regexp {self.text} is INVALID!")

class RegularExpression(models.Model):
    """
    RegularExpressions are written as strict patterns (model is not trained on them?
    @Daniil Cherniavskii )
    """
    parent_intent = models.ForeignKey(
        Intent,
        on_delete=models.CASCADE,
        related_name="reg_phrases"
    )

    text = models.CharField(max_length=2000)

    def clean(self):
        # print("Clean validation is called")
        if self.text:
            try:
                re.compile(self.text)
                # print("regexp is valid")
            except re.error:
                raise ValidationError(f"WARNING: regexp {self.text} is INVALID!")


class PunctuationElement(models.Model):
    parent_intent = models.ForeignKey(
        Intent,
        on_delete=models.CASCADE,
        related_name="punctuation"
    )

    text = models.CharField(max_length=1)

# class ICDataset(models.Model):
#     # like "ontonotes2003.train", "ontonotes2003.valid"
#     name = models.CharField(max_length=2000)
#
#     def produce_conll(self, aFilepath):
#         pass
#
#     def collect_samples(self):
#         pass
#
#     def load_from_conll_file(self, aFilepath):
#         pass

from ic_dataset.tasks import dp_retrain_task

# Signal receiver
@receiver(signals.post_save, sender=Intent)
def retrain_intent_catcher_model(sender, instance, created, **kwargs):
    print("Intent save method is called")
    from celery import app as cel_app
    # print(cel_app.__dict__)
    # cel_app.loader.import_default_modules()
    # all_task_names = cel_app.tasks.keys()
    # all_tasks = cel_app.tasks.values()
    print("celery info:")
    # print(all_task_names)
    # print(all_tasks)
    print("____")

    dp_retrain_task.delay()
    print("Request for model retraining is set...")
