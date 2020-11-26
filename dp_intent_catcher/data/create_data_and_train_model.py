#!/usr/bin/env python
import os
import json
import argparse
import tensorflow as tf
import tensorflow_hub as hub
from collections import OrderedDict
from utils import *

DP_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
# TODO make configurable?
MODELS_DIR = DP_DATA_DIR + "/models"
METRICS_DIR = DP_DATA_DIR + '/metrics'
# TODO outputting model to remote ssh feature support
# model configs:
MULTILABEL = True
TRAIN_SIZE = 0.5
DENSE_LAYERS = 1


# Create metrics directory if not exists
if not os.path.exists(METRICS_DIR):
    os.makedirs(METRICS_DIR)

USE_MODEL_PATH = os.environ.get('USE_MODEL_PATH', None)
if USE_MODEL_PATH is None:
    USE_MODEL_PATH = 'https://tfhub.dev/google/universal-sentence-encoder/1'

TFHUB_CACHE_DIR = os.environ.get('TFHUB_CACHE_DIR', None)
if TFHUB_CACHE_DIR is None:
    os.environ['TFHUB_CACHE_DIR'] = DP_DATA_DIR + '/tfhub_model'


def create_data_and_train_model(intent_phrases_path, model_path, epochs=7, model_name=None):
    """
    Generates dataset then trains and saves model
    :param model_name: str
    :param intent_phrases_path: str like "intent_phrases.json"
    :param model_path: str: path to the dir with the model files. created if not exist. Overwritten if not empty
    :param epochs:
    :return:
    """

    if not os.path.exists(model_path):
        os.makedirs(model_path)

    if not model_name:
        model_name = model_path.split("/")[-1]
        print("model_name")
        print(model_name)

    use = hub.Module(USE_MODEL_PATH)

    with open(intent_phrases_path, 'r') as fp:
        all_data = json.load(fp)
        intent_phrases = OrderedDict(all_data['intent_phrases'])
        random_phrases = all_data['random_phrases']

    intent_data = {}
    intents = sorted(list(intent_phrases.keys()))
    print("Creating  data...")
    print("Intent: number of original phrases")
    with tf.compat.v1.Session() as sess:
        sess.run([tf.compat.v1.global_variables_initializer(),
                  tf.compat.v1.tables_initializer()])

        for intent, data in intent_phrases.items():
            # todo set limit by the most populated class
            phrases = generate_phrases(data['phrases'], data['punctuation'], limit=200)
            intent_data[intent] = {
                'generated_phrases': phrases,
                'num_punctuation': len(data['punctuation']),
                'min_precision': data['min_precision']
            }
            print(f"{intent}: {len(phrases) // len(data['punctuation'])}")
        print("Generating embeddings...")
        intent_embeddings_op = {intent: use(sentences['generated_phrases'])
                                for intent, sentences in intent_data.items()}

        random_preembedded = generate_phrases(
            random_phrases['phrases'], random_phrases['punctuation'])
        random_embeddings_op = use(random_preembedded)

        intent_embeddings = sess.run(intent_embeddings_op)
        random_embeddings = sess.run(random_embeddings_op)

        for intent in intents:
            intent_data[intent] = {
                'embeddings': intent_embeddings[intent].tolist(),
                'min_precision': intent_data[intent]['min_precision'],
                'num_punctuation': intent_data[intent]['num_punctuation']
            }

    print("Created!")

    random_embeddings = random_embeddings.tolist()

    print("Scoring model...")

    metrics, thresholds = score_model(
        intent_data,
        intents,
        random_embeddings,
        samples=3,
        # samples=20,
        dense_layers=DENSE_LAYERS,
        epochs=int(epochs),
        train_size=TRAIN_SIZE,
        multilabel=MULTILABEL
    )

    metrics.to_csv(METRICS_DIR +"/"+model_name+'_metrics.csv')
    print("METRICS:")
    print(metrics)

    print("Training model...")
    train_data = get_train_data(
        intent_data, intents, random_embeddings, multilabel=MULTILABEL
    )
    model = get_linear_classifier(
        intents, dense_layers=DENSE_LAYERS, use_metrics=False, multilabel=MULTILABEL
    )

    model.fit(
        x=train_data['X'],
        y=train_data['y'],
        epochs=int(epochs)
    )
    print(f"Saving model to: {model_path}")

    print("model_path")
    print(model_path)

    modle_clf_file_path = model_path + "/linear_classifier.h5"
    model.save(modle_clf_file_path)
    INTENT_DATA_PATH = model_path + '/intent_data.json'

    print(f"Saving thresholds to: {INTENT_DATA_PATH}")
    json.dump(thresholds, open(INTENT_DATA_PATH, 'w'))

    # we also need to save intent_phrases.json into output
    try:
        from shutil import copyfile
        copyfile(intent_phrases_path, model_path+"/intent_phrases.json")
    except Exception as e:
        print("Skipping copying intent_phrases.json because of exception:")
        print(e)
    print(f"Model successfully saved to: {model_path}!")
    return model_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # python data/create_data_and_train_model.py --intent_phrases_path data/intent_phrases_mini.json --model_path ./models/new_ic/
    parser.add_argument(
        "--intent_phrases_path", help="file with phrases for embedding generation", default='intent_phrases.json')
    parser.add_argument(
        '--model_path', help='path where to save the model', default=MODELS_DIR + '/default_model')
    parser.add_argument(
        '--epochs', help='number of epochs to train model', default=7)
    # Whereas to calc metrics or not (default value = True)
    args = parser.parse_args()

    # main()
    create_data_and_train_model(intent_phrases_path=args.intent_phrases_path,
                                model_path=args.model_path,
                                epochs=args.epochs)
    print("Fin.")