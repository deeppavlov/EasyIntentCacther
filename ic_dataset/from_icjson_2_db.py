"""
Скрипт конвертит тренировочные экземпляры в базу из файла в ConLL2003 разметке для задачи NER
"""
################# Universal Import ###################################################
import sys
import os
import argparse
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(ROOT_DIR)
sys.path.append(ROOT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EasyIntentCatcher.settings")
import django
django.setup()
# #####################################################
from copy import copy
import json

# from ner_dataset.models import TrainingSample, NERDataset
# from deeppavlov.dataset_readers.conll2003_reader import Conll2003DatasetReader
# from deeppavlov.core.data.data_learning_iterator import DataLearningIterator
# from deeppavlov.core.commands.utils import expand_path, import_packages, parse_config
# from deeppavlov.core.trainers.nn_trainer import NNTrainer
# from deeppavlov.core.commands.train import read_data_by_config
from ic_dataset.models import Intent, PhraseExpression, PunctuationElement, RegularExpression
# config_path = "/home/alx/Cloud/DeepPavlov/EasyNER/EasyNER/deep_pavlov_ner/configs/ner_ontonotes.json"
# config_path = "/home/alx/Workspace/EasyIntentCatcher/EasyNER/deep_pavlov_ner/configs/ner_ontonotes.json"
ds_path = "/home/alx/Workspace/EasyIntentCatcher/dp_intent_catcher/data/intent_phrases.json"

# config = parse_config(config_path)
# creader = Conll2003DatasetReader(data_path=ds_path)

# data = read_data_by_config(config)
# dli = DataLearningIterator(data=data, shuffle=False)
# print(config)
# trainer = NNTrainer(config['chainer'])
# trainer.train(dli)

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
    intent_names = ic_data['intent_phrases'].keys()
    # import ipdb;ipdb.set_trace()
    for intent_name, intent_data in ic_data['intent_phrases'].items():
        intnt = update_db_from_intent_data(intent_name, intent_data)

    # special random intent:
    rndm_intnt = 'random_phrases'
    rndm_intnt = update_db_from_intent_data(rndm_intnt, ic_data[rndm_intnt])
    # TODO informa about updates?

if __name__=="__main__":

    with open(ds_path, "r") as js_file:

        data = json.load(js_file)
        print(data)
        intent_names = data['intent_phrases'].keys()
        # import ipdb;ipdb.set_trace()
        for intent_name, intent_data in data['intent_phrases'].items():

            intnt = update_db_from_intent_data(intent_name, intent_data)

        # special random intent:
        rndm_intnt = 'random_phrases'
        rndm_intnt = update_db_from_intent_data(rndm_intnt, data[rndm_intnt])
        # data['random_phrases']['phrases']
        # data['random_phrases']['punctuation']

    print("Dumping the file ")
    #
    # for each_datum in dli.gen_batches(batch_size=1):
    #     # print(each_datum)
    #     # list of tokens:
    #     # print(each_datum[0][0])
    #     toks = each_datum[0][0]
    #     initial_sentence = " ".join(toks)
    #     # list of codes:
    #     # print(each_datum[1][0])
    #     bio_toks = each_datum[1][0]
    #     markup_str = " ".join(bio_toks)
    #     obj, created = TrainingSample.objects.get_or_create(
    #         input_data=initial_sentence, golden_label=markup_str)
    #     if created:
    #         print(f"{obj} was created")
    #     else:
    #         print(f"{obj} is in DB")
    #     print("__")
    # print("Fin.")
