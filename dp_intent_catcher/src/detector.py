#!/usr/bin/env python

import os
from itertools import chain

import json
from typing import List

import re
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub
from copy import copy
from collections import defaultdict
############################################# Universal Import ##################################
import os, inspect, sys
current_abs_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
# global_CTS_path = os.path.dirname(os.path.dirname(os.path.dirname(current_abs_path)))
INTENT_CATCHER_PATH = os.path.dirname(os.path.dirname(current_abs_path))
print("INTENT CACTHER PATH")
print(INTENT_CATCHER_PATH)
# if global_CTS_path not in sys.path:
#     sys.path.append(global_CTS_path)
# ################################################################################################
#
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CTSProject.settings')
# django.setup()


USE_MODEL_PATH = os.environ.get('USE_MODEL_PATH', None)
if USE_MODEL_PATH is None:
    USE_MODEL_PATH = 'https://tfhub.dev/google/universal-sentence-encoder/1'

INTENT_MODEL_PATH = os.environ.get('INTENT_MODEL_PATH', None)
if INTENT_MODEL_PATH is None:
    INTENT_MODEL_PATH = INTENT_CATCHER_PATH +'/data/models/linear_classifier_h1.h5'

INTENT_DATA_PATH = os.environ.get('INTENT_DATA_PATH', None)


if INTENT_DATA_PATH is None:
    INTENT_DATA_PATH = INTENT_CATCHER_PATH + '/data/intent_data.json'
    # INTENT_DATA_PATH = '/data/intent_data.json'

INTENT_PHRASES_PATH = os.environ.get('INTENT_PHRASES_PATH', None)
if INTENT_PHRASES_PATH is None:
    INTENT_PHRASES_PATH = INTENT_CATCHER_PATH + '/data/intent_phrases.json'
    # INTENT_PHRASES_PATH = '/data/intent_phrases.json'

TFHUB_CACHE_DIR = os.environ.get('TFHUB_CACHE_DIR', None)
if TFHUB_CACHE_DIR is None:
    os.environ['TFHUB_CACHE_DIR'] = INTENT_CATCHER_PATH + '/data/tfhub_cache'

os.environ['TF_XLA_FLAGS'] = '--tf_xla_cpu_global_jit'  # Don't know that is


class AbstractDetector:

    def __init__(self, logger):
        self.logger = logger

    def detect(self, utterances: List, sess):
        raise NotImplementedError("Detect method not implemented!")


class ClassifierDetector(AbstractDetector):
    """
    Linear intent classifier based on USE embeddings.
    Current configuration is one linear layer upon USE embedding.

    """

    def __init__(self, logger, intent_model_dir_path, USE_model_URL):
        super().__init__(logger)
        # TODO unify with refs in create_data_and_train_model.py:
        intent_data_path = intent_model_dir_path + "/intent_data.json"
        intent_model_path = intent_model_dir_path + "/linear_classifier.h5"
        self.intent_model_dir_path = intent_model_dir_path
        self.data = json.load(open(intent_data_path))
        if 'random' in self.data.keys():
            self.data.pop('random')
        self.intents = sorted(list(self.data.keys()))
        self.embedder = hub.Module(USE_model_URL)

        self.model = tf.keras.models.load_model(intent_model_path)
        self.sentences = tf.compat.v1.placeholder(dtype=tf.string)
        self.embedded_sentences = self.embedder(self.sentences)

    def detect(self, utterances: List, sess):
        self.logger.info(f"All utterances: {utterances}")
        len_sentences = [len(utt) for utt in utterances]
        tok_sentences = list(chain.from_iterable(utterances))
        embedded_sentences = sess.run(self.embedded_sentences, feed_dict={
                                      self.sentences: tok_sentences})

        predictions = self.model.predict(embedded_sentences)
        predictions_class = np.argmax(predictions, axis=1)
        prediction_confidence = np.max(predictions, axis=1)
        predictions = list(zip(predictions_class, prediction_confidence))

        i = 0
        detected_confidence = []
        for utt, l in zip(utterances, len_sentences):
            self.logger.info(f"Utterance: {utt}\nLength: {l}")
            ans = {}
            prediction = [(self.intents[j], conf)
                          for j, conf in predictions[i:i + l] if j < len(self.intents)]
            confidences = defaultdict(int)
            detected = {intent for intent, conf in prediction}
            for intent, conf in prediction:
                confidences[intent] = max(conf, confidences[intent])
            for intent in self.intents:
                logger_line = f"Intent: {intent}    "
                logger_line += f"prediction: {round(float(confidences[intent]), 3)}, detect: {int(intent in detected)}"
                self.logger.info(logger_line)

            ans = {intent: {'detected': int(intent in detected),
                            'confidence': float(confidences[intent])} for intent in self.intents}
            detected_confidence.append(ans)
            i += l
        return detected_confidence


class MultilabelDetector(AbstractDetector):
    """
    Multilabel linear intent classifier based on USE embeddings.
    Current configuration is one linear layer upon USE embedding.

    """

    def __init__(self, logger, intent_model_dir_path, USE_model_URL):
        super().__init__(logger)
        intent_data_path = intent_model_dir_path + "/intent_data.json"
        intent_model_path = intent_model_dir_path + "/linear_classifier.h5"
        self.data = json.load(open(intent_data_path))
        if 'random' in self.data:
            self.data.pop('random')
        self.intents = sorted(list(self.data.keys()))
        self.thresholds = np.array([self.data[intent]
                                    for intent in self.intents])
        self.embedder = hub.Module(USE_model_URL)
        self.model = tf.keras.models.load_model(intent_model_path)
        self.sentences = tf.compat.v1.placeholder(dtype=tf.string)
        self.embedded_sentences = self.embedder(self.sentences)

    def glue_utterances_up(self, prediction):
        return list(chain.from_iterable(prediction))

    def detect(self, utterances: List, sess):
        self.logger.info(f"All utterances: {utterances}")
        len_sentences = [len(utt) for utt in utterances]
        tok_sentences = list(chain.from_iterable(utterances))
        if len(tok_sentences) == 0:
            return [{intent: {'detected': 0,
                              'confidence': 0.0} for intent in self.intents} for i in range(len(utterances))]
        embedded_sentences = sess.run(self.embedded_sentences, feed_dict={
                                      self.sentences: tok_sentences})

        predictions = self.model.predict(embedded_sentences)

        i = 0
        detected_confidence = []
        for utt, ls in zip(utterances, len_sentences):
            self.logger.info(f"Utterance: {utt}\nLength: {ls}")
            ans = {}
            if ls == 0:
                ans = {intent: {'detected': 0,
                                'confidence': 0.0} for intent in self.intents}
                detected_confidence.append(ans)
                continue
            prediction = [[(self.intents[j], p[j]) for j in np.argwhere(p > self.thresholds).reshape(-1)]
                          for p in predictions[i:i + ls]]
            prediction = self.glue_utterances_up(prediction)
            confidences = defaultdict(float)
            detected = {intent for intent, conf in prediction}
            for intent, conf in prediction:
                confidences[intent] = max(conf, confidences[intent])
            for intent in self.intents:
                logger_line = f"Intent: {intent}    "
                logger_line += f"prediction: {round(float(confidences[intent]), 3)}, detect: {int(intent in detected)}"
                self.logger.info(logger_line)

            ans = {intent: {'detected': int(intent in detected),
                            'confidence': float(confidences[intent])} for intent in self.intents}
            detected_confidence.append(ans)
            i += ls
        return detected_confidence


class MultilabelDetectorWithIntentHierarchy(MultilabelDetector):
    """
    Multilabel linear intent classifier with intent priorities based on USE embeddings.
    Current configuration is one linear layer upon USE embedding.

    Intent priorities: choose intents from the last utterance in human sentence.
    """

    def __init__(self, logger, intent_model_dir_path, USE_model_URL):
        super().__init__(logger)
        self.intent_priorities = [
            'exit',
            'repeat',
            'cant_do',
            'dont_understand',
            'topic_switching'
        ]

    def glue_utterances_up(self, prediction):
        result = []
        for utt in prediction[::-1]:
            if len(utt) != 0:
                result = utt  # Get the last utterance with intent
        for target_intent in self.intent_priorities:  # Filter out intents by priority
            if any([intent == target_intent for intent, conf in result]) and len(result) > 1:
                result = [(intent, conf)
                          for intent, conf in result if intent != target_intent]
        return result


class RegMD(MultilabelDetector):
    """
    Multilabel linear intent classifier based on USE embeddings
    and regexp check.
    Current configuration is one linear layer upon USE embedding.

    Intent priorities: choose intents from the last utterance in human sentence.
    """

    def __init__(self, logger, intent_model_dir_path, USE_model_URL=None):
        if not USE_model_URL:
            USE_model_URL = USE_MODEL_PATH
        super().__init__(logger, intent_model_dir_path, USE_model_URL)
        intent_phrases_path = intent_model_dir_path + "/intent_phrases.json"
        self.regexp = {intent: list(
            chain.from_iterable(
                [[phrase + "\\" + punct for phrase in data['phrases']] for punct in data['punctuation']]
            )
        ) + data.get('reg_phrases', [])
            for intent, data in json.load(open(intent_phrases_path))['intent_phrases'].items()}
        self.regexp = {intent: [re.compile(phrase) for phrase in phrases]
                       for intent, phrases in self.regexp.items()}

    def unite_responses(self, responses_a, responses_b):
        assert len(responses_a) == len(responses_b), self.logger.error(
            "Responses have unequal lengths!")
        result = []
        for a, b in zip(responses_a, responses_b):
            resp = {}
            for intent in a:
                resp[intent] = {
                    'detected': max(a[intent]['detected'], b[intent]['detected']),
                    'confidence': max(a[intent]['confidence'], b[intent]['confidence'])
                }
            result.append(resp)
        return result

    def detect(self, utterances: List, sess):
        responds = []
        not_detected_utterances = []
        for utterance in utterances:
            resp = {
                intent: {
                    'detected': 0,
                    'confidence': 0.0
                } for intent in self.intents
            }
            # not_detected_utterance = utterance.copy()
            not_detected_utterance = copy(utterance)
            for intent, regs in self.regexp.items():
                for i, utt in enumerate(utterance):
                    for reg in regs:
                        if reg.fullmatch(utt):
                            resp[intent]['detected'] = 1
                            resp[intent]['confidence'] = 1.0
                            not_detected_utterance[i] = None
                            break
            not_detected_utterance = [
                utt for utt in not_detected_utterance if utt]
            not_detected_utterances.append(not_detected_utterance)
            responds.append(resp)
        use_responds = super().detect(not_detected_utterances, sess)
        return self.unite_responses(use_responds, responds)
