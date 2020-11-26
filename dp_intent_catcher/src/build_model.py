#!/usr/bin/env python
import os, inspect, sys
import glob
from os import getenv
import tensorflow as tf
import logging

from .detector import *

# sentry_sdk.init(getenv('SENTRY_DSN'))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class IntentCatcherClassifier():
    def __init__(self):
        self.sess = tf.compat.v1.Session()
        logger.info('Creating detector...')
        ############################################# Universal Import ##################################
        current_abs_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
        DP_INTENT_CATCHER_PATH = os.path.dirname(os.path.dirname(current_abs_path))
        # print("DP_INTENT_CATCHER_PATH ")
        # print(DP_INTENT_CATCHER_PATH )

        search_dir = DP_INTENT_CATCHER_PATH + "/data/models/*"
        # print(search_dir)
        dirs = list(filter(os.path.isdir, glob.glob(search_dir)))
        paths = sorted(dirs, key=lambda x: os.path.getmtime(x))
        print("Found models:")
        print(paths)

        # try to open any model that can be opened. By the newest:
        for model_dir_path in paths:
            try:
                self.detector = RegMD(logger, intent_model_dir_path=model_dir_path)
                logger.info('Creating detector... finished')

                logger.info('Initializing tf variables...')
                self.sess.run(tf.compat.v1.tables_initializer())

                logger.info("Tables initialized")
                self.sess.run(tf.compat.v1.global_variables_initializer())
                logger.info("Global variables initialized")

                # self.detector.detect([["Wake up phrase"]], self.sess)
                logger.info(f"Intent Cacther initialization is done for {model_dir_path}!")
                print(f"Model is launched: {model_dir_path}")
                break
            except Exception as e:
                print(e)
        else:
            # print(no models found, launch default:
            print("can not launch any model!")
            raise Exception("No model launchable")


    def predict(self, utterance):
        # TODO detect if model updated
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