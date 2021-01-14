import os
from celery import Celery, Task
from django.core.cache import cache
from celery.utils.log import get_task_logger
from celery import shared_task
################# Universal Import ###################################################
import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EasyIntentCatcher.settings")
import django
django.setup()
# #####################################################
logger = get_task_logger(__name__)

celery = Celery('tasks')


@shared_task()
def dp_retrain_task():
    """
    Task which generates dataset from DB,
    then it launches training of the model
    """
    from ic_dataset.from_db_2_icjson import export_db_2_ic_json
    from ic_dataset.models import calc_dataset_hash
    print("Retraining")
    hash = calc_dataset_hash()
    # model_path = "dp_intent_catcher/data/models/autocreated_model"
    model_path = f"dp_intent_catcher/data/models/{hash}"
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    else:
        # TODO check if model is really trained and workable?
        # print("Path for model exist then no changes happened no need to retrain? Exiting.")
        # return
        print(f"Path for model exist: {model_path}. Retraining")

    print("Exporting dataset file...")
    # TODO refactor multiuse of ds path?
    ds_path = model_path + "/intent_phrases.json"
    export_db_2_ic_json(ds_path)
    print("Exported. Start adding op")
    # TODO cancel/kill all ongoing training tasks
    # https://docs.celeryproject.org/en/latest/reference/celery.contrib.abortable.html
    from prediction_models.trainer import Trainer

    try:
        print("Runing trainer")
        model = Trainer.train_model(intent_phrases_path=ds_path, model_path=model_path, model_name=hash)

        print(model)
        # but may be not successfull
        print("Training is completed.")
        # TODO call the hook!
    except Exception as e:
        print(e)
        print("Something gone wrong in training")
    print("Task Fin!")

@shared_task
def xsum(numbers):
    return sum(numbers)

# deprecated
@shared_task()
def dp_retrain_task_cli():
    """
    Task which generates dataset from DB,
    then it launches training of the model
    """
    from ic_dataset.from_db_2_icjson import export_db_2_ic_json
    from ic_dataset.models import calc_dataset_hash

    hash = calc_dataset_hash()
    # model_path = "dp_intent_catcher/data/models/autocreated_model"
    model_path = f"dp_intent_catcher/data/models/{hash}"
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    else:
        # TODO check if model is really trained and workable?
        # print("Path for model exist then no changes happened no need to retrain? Exiting.")
        # return
        print(f"Path for model exist: {model_path}. Retraining")

    print("Exporting dataset file...")
    # TODO refactor multiuse of ds path?
    ds_path = model_path + "/intent_phrases.json"
    export_db_2_ic_json(ds_path)
    print("Exported. Start adding op")
    # TODO cancel/kill all ongoing training tasks
    # https://docs.celeryproject.org/en/latest/reference/celery.contrib.abortable.html
    # retrain
    try:
        import subprocess
        # TODO run as direct function?
        results = subprocess.run([
            "python", "dp_intent_catcher/data/create_data_and_train_model.py",
            "--intent_phrases_path", ds_path,
            "--model_path", model_path
            ],
            stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(results)
        # but may be not successfull
        print("Training is completed.")
        # TODO call the hook!
    except Exception as e:
        print(e)
        print("Something gone wrong in training")
    print("Task Fin!")