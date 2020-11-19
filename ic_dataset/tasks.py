from celery import Celery, Task
from django.core.cache import cache
from celery.utils.log import get_task_logger
from celery import shared_task

logger = get_task_logger(__name__)


class SingletonTask(Task):
    def __call__(self, *args, **kwargs):
        lock = cache.lock(self.name)

        if not lock.acquire(blocking=False):
            print("{} failed to lock".format(self.name))
            logger.info("{} failed to lock".format(self.name))
            return

        try:
            super(SingletonTask, self).__call__(*args, **kwargs)
        except Exception as e:
            print("Releasing lock")
            logger.info("Releasing lock")
            lock.release()
            raise e
        lock.release()


# app = Celery('tasks', broker='pyamqp://guest@localhost//')
#
# @app.task
# def add(x, y):
#     print(f"Adding {x} to {y}")
#     return x + y
#
#
# # @shared_task(base=SingletonTask)
# @app.task(base=SingletonTask)
# def test_task():
#     from time import sleep
#     print("Slleeep task")
#     sleep(10)


# @app.task(base=SingletonTask)
@shared_task(base=SingletonTask)
def dp_retrain_task():
    """
    Task which generates dataset from DB
    then launches trainig of the model
    :return:
    """

    # TODO check that dataset actually changed
    # TODO get all tasks?
    from celery import app as cel_app
    print(cel_app.__dict__)
    # cel_app.loader.import_default_modules()
    # all_task_names = cel_app.tasks.keys()
    # all_tasks = cel_app.tasks.values()
    # print("celery info:")
    # print(all_task_names)
    # print(all_tasks)
    print("____")
    # TODO generate json: data/intent_phrases.json from DB data
    from ic_dataset.from_db_2_icjson import export_db_2_ic_json, ds_path
    print("Expoerting dataset file")
    export_db_2_ic_json(ds_path)
    print("Exported. Start adding op")
    ggg = True
    if ggg:
        return
    # +++++
    # retrain
    # TODO stop all pending training tasks
    # https://docs.celeryproject.org/en/latest/reference/celery.contrib.abortable.html
    # TODO add task for model training
    # stop current task and start the new?
    try:
        import subprocess
        # result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
        # results = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        model_path = "dp_intent_catcher/data/models/autocreated_model"
        # TODO run as direct function?
        results = subprocess.run([
            "python", "dp_intent_catcher/data/create_data_and_train_model.py",
            "--intent_phrases_path", ds_path,
            "--model_path", model_path
        ],
            # "dp_intent_catcher/data/intent_phrases_export.json"],
            stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(results)
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