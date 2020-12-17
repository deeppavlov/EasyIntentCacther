"""
Script produces intent_phrases.json file from DB Training Samples
"""
import json
from copy import copy
################# Universal Import ###################################################
import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EasyIntentCatcher.settings.local")
import django
django.setup()
# #####################################################
from ic_dataset.models import Intent, PhraseExpression, PunctuationElement, RegularExpression


def export_db_2_ic_json(target_json_path):
    inents = Intent.objects.all()
    # template for json
    output_json = {
        "random_phrases": {},
        "intent_phrases": {}
    }
    for each_int in inents:
        if each_int.intent_name=="random_phrases":
            # special case:
            # TODO refactor format of dataset to make random intent as any other?
            output_json["random_phrases"]["phrases"] = [ph.text for ph in each_int.phrases.all()]
            output_json["random_phrases"]["punctuation"] = [ph.text for ph in each_int.punctuation.all()]
            output_json["random_phrases"]["reg_phrases"] = [ph.text for ph in each_int.reg_phrases.all()]
        else:
            # basic case:
            output_json['intent_phrases'][each_int.intent_name] = {}
            output_json['intent_phrases'][each_int.intent_name]['phrases'] = [ph.text for ph in each_int.phrases.all()]
            output_json['intent_phrases'][each_int.intent_name]["punctuation"] = [ph.text for ph in each_int.punctuation.all()]
            output_json['intent_phrases'][each_int.intent_name]["reg_phrases"] = [ph.text for ph in each_int.reg_phrases.all()]
            output_json['intent_phrases'][each_int.intent_name]["min_precision"] = each_int.min_precision

        # print(json.dumps(output_json, indent=4, sort_keys=True))
        with open(target_json_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, ensure_ascii=False, indent=4, sort_keys=True)

if __name__=="__main__":
    """
    python ic_dataset/from_db_2_icjson.py
     
    """
    # TODO add argument to specify output file!
    ds_path = ROOT_DIR + "/dp_intent_catcher/data/intent_phrases_export.json"
    print(f"Starting export to {ds_path}")
    export_db_2_ic_json(target_json_path=ds_path)
    print("writing file target_json_path completed!")
    print("Fin.")