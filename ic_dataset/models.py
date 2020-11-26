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


import hashlib

def calc_dataset_hash():
    """
    Collects all data for dataset and generates hash of it
    :return: hash of the dataset
    """
    # get all phrases and regexps and punctuations and calc their hash
    phrases = [ph.text for ph in PhraseExpression.objects.all()]
    regexs = [regx.text for regx in RegularExpression.objects.all()]
    puncts = [pe.text for pe in PunctuationElement.objects.all()]

    phrases_str = ", ".join(phrases)
    regexs_str = ", ".join(regexs)
    puncts_str = ", ".join(puncts)
    merged_text = f"{phrases_str} {regexs_str} {puncts_str}"

    hash_object = hashlib.md5(merged_text.encode())
    hash_val = hash_object.hexdigest()
    print("Datset hash_val")
    print(hash_val)
    return hash_val

# from ic_dataset.tasks import dp_retrain_task
#
# # Signal receiver
# @receiver(signals.post_save, sender=Intent)
# def retrain_intent_catcher_model(sender, instance, created, **kwargs):
#     print("Intent save method is called")
#     # hash = calc_dataset_hash()
#     # dp_retrain_task.delay()
#     print("Request for model retraining is set...")
