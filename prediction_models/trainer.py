from prediction_models.models import PredictionModel
import dp_intent_catcher.data.create_data_and_train_model
from .ssh_utils import upload_to_ssh_recursive


class Trainer():
    """Class responsible for model preparation and loging into DB"""
    @classmethod
    def train_model(cls, intent_phrases_path, model_path, epochs=7, model_name=None):
        """Trains model in Django context (with adding model entry into DB)"""
        print("training model")
        pm, created = PredictionModel.objects.get_or_create(model_hash_code=model_name, storage_path=model_path)
        # if not created:
        #     exisitng model
        pm.state = PredictionModel.STATE_ON_TRAIN
        pm.save()
        try:
            model = dp_intent_catcher.data.create_data_and_train_model.create_data_and_train_model(intent_phrases_path, model_path, epochs, model_name)
            print("Training completed")
        except Exception as e:
            print("Exception during training:")
            print(e)
            pm.state = PredictionModel.STATE_FAILED
            pm.save()
        else:
            pm.state = PredictionModel.STATE_TRAINED
            pm.save()
            upload_to_ssh_recursive(model_path)
            print("SSH export completed!")
        # TODO validate that it trained and reproducible?

        return pm

