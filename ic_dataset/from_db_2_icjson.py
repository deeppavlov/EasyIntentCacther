"""
Script produces CONNL2003 file from DB Training Samples
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
ds_path = "/home/alx/Cloud/aiml_related/EasyIntentCatcher/dp_intent_catcher/data/intent_phrases_export.json"

def export_db_2_ic_json(target_json_path):

    inents = Intent.objects.all()
    # template for json
    output_json = {
        "random_phrases": {},
        "intent_phrases": {}
    }
    # for each_ts in ts[:100]:
    for each_int in inents:
        if each_int.intent_name=="random_phrases":
            # special case:
            # TODO refactor format of dataset to make random intent as any other?
            # print(each_int.intent_name)
            # print("each_int.phrases")
            # print(each_int.phrases)
            output_json["random_phrases"]["phrases"] = [ph.text for ph in each_int.phrases.all()]
            output_json["random_phrases"]["punctuation"] = [ph.text for ph in each_int.punctuation.all()]
            output_json["random_phrases"]["reg_phrases"] = [ph.text for ph in each_int.reg_phrases.all()]

        else:
            # basic case:
            # print(each_int.intent_name)
            # print("each_int.phrases")
            # print(each_int.phrases)
            # phrases

            output_json['intent_phrases'][each_int.intent_name] = {}
            output_json['intent_phrases'][each_int.intent_name]['phrases'] = [ph.text for ph in each_int.phrases.all()]
            output_json['intent_phrases'][each_int.intent_name]["punctuation"] = [ph.text for ph in each_int.punctuation.all()]
            output_json['intent_phrases'][each_int.intent_name]["reg_phrases"] = [ph.text for ph in each_int.reg_phrases.all()]
            output_json['intent_phrases'][each_int.intent_name]["min_precision"] = each_int.min_precision

        print("__"*80)
        print(json.dumps(output_json, indent=4, sort_keys=True))

        with open(target_json_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, ensure_ascii=False, indent=4, sort_keys=True)
        print("__"*80)

if __name__=="__main__":
    """
    python ic_dataset/from_db_2_icjson.py
     
    """
    # TODO add argument to specify output file!
    print(f"Starting export to {ds_path}")
    export_db_2_ic_json(target_json_path=ds_path)
    print("writing file target_json_path completed!")
    print("Fin.")