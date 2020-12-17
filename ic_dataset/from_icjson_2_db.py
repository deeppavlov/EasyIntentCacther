"""
Скрипт конвертит тренировочные экземпляры в базу из файла в ConLL2003 разметке для задачи NER
"""
################# Universal Import ###################################################
import sys
import os
import argparse
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EasyIntentCatcher.settings.local")
import django
django.setup()
# #####################################################
from copy import copy
import json
from ic_dataset.models import Intent, PhraseExpression, PunctuationElement, RegularExpression


def update_db_from_intent_data(intent_name, intent_data):
    intnt, is_created = Intent.objects.get_or_create(intent_name=intent_name)
    # if not is_created:
    #     # TODO implement update of child elements?
    #     return intnt

    if 'min_precision' in intent_data and intnt.min_precision != intent_data['min_precision']:
        intnt.min_precision = intent_data['min_precision']
        intnt.save()

    # analyze intent data
    if 'phrases' in intent_data:
        for phrase in intent_data['phrases']:
            PhraseExpression.objects.get_or_create(text=phrase, parent_intent=intnt)

    if 'reg_phrases' in intent_data:
        for phrase in intent_data['reg_phrases']:
            RegularExpression.objects.get_or_create(text=phrase, parent_intent=intnt)

    if 'punctuation' in intent_data:
        for phrase in intent_data['punctuation']:
            PunctuationElement.objects.get_or_create(text=phrase, parent_intent=intnt)

    return intnt


def update_from_ic_ds_formatted_dict(ic_data):
    # intent_names = ic_data['intent_phrases'].keys()
    for intent_name, intent_data in ic_data['intent_phrases'].items():
        intnt = update_db_from_intent_data(intent_name, intent_data)

    # special random intent:
    rndm_intnt = 'random_phrases'
    rndm_intnt = update_db_from_intent_data(rndm_intnt, ic_data[rndm_intnt])
    # TODO informa about updates?


if __name__=="__main__":
    # TODO add args parsing? But do we need CLI operation for importing to DB?
    ds_path = ROOT_DIR + "/dp_intent_catcher/data/intent_phrases.json"
    print(f"Dumping the file {ds_path}")
    with open(ds_path, "r") as js_file:
        data = json.load(js_file)
        print(data)
        update_from_ic_ds_formatted_dict(data)
        # intent_names = data['intent_phrases'].keys()
        # for intent_name, intent_data in data['intent_phrases'].items():
        #     intnt = update_db_from_intent_data(intent_name, intent_data)
        # # special random intent:
        # rndm_intnt = 'random_phrases'
        # rndm_intnt = update_db_from_intent_data(rndm_intnt, data[rndm_intnt])
        # data['random_phrases']['phrases']
        # data['random_phrases']['punctuation']
    print("Fin.")
