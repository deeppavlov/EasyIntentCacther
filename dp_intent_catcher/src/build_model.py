#!/usr/bin/env python

from os import getenv

import tensorflow as tf
import logging
# import sentry_sdk
from flask import Flask, request, jsonify

from .detector import *

# sentry_sdk.init(getenv('SENTRY_DSN'))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class IntentCatcherClassifier():
    def __init__(self):
        self.sess = tf.compat.v1.Session()

        logger.info('Creating detector...')
        self.detector = RegMD(logger)
        logger.info('Creating detector... finished')

        logger.info('Initializing tf variables...')
        self.sess.run(tf.compat.v1.tables_initializer())

        logger.info("Tables initialized")
        self.sess.run(tf.compat.v1.global_variables_initializer())
        logger.info("Global variables initialized")

        # self.detector.detect([["Wake up phrase"]], self.sess)
        logger.info("DONE")

    def predict(self, utterance):
        # utterances = "My friend want to talk about basketball"
        # logger.info(f"Number of utterances: {len(utterances)}")
        results = self.detector.detect(utterance, self.sess)
        print("results:")
        print(results)
        return results

    def __call__(self, *args, **kwargs):
        return self.predict(*args, **kwargs)

model_instance = None

def get_prepared_model():
    #TODO make singleton?
    global model_instance
    if not model_instance:
        model_instance = IntentCatcherClassifier()
    return model_instance