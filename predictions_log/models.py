from django.db import models


class PredictionCase(models.Model):
    """
    Unique by input-prediction pair

    """
    input_data = models.CharField(max_length=2000)
    # result of prediction
    prediction_data = models.CharField(max_length=2000)

    # TODO make json field?:
    other_kwargs = models.CharField(max_length=2000, null=True, default=None)

    # created_by = ref to model
    created_at = models.DateTimeField('date occured', auto_now_add=True)
    last_updated_at = models.DateTimeField('last date occured', auto_now=True)

    # count of events occurences
    count = models.IntegerField('count', default=1)

    def __str__(self):
        return f"{self.input_data}//{self.prediction_data}"
#
# class PredictionEvent(models.Model):
#     input_data = models.CharField(max_length=2000)
#     # result of prediction
#     prediction_data = models.CharField(max_length=2000)
#
#     # created_by = ref to model
#     created_at = models.DateTimeField('date occured', auto_now_add=True)
#     # if the case is validated by Human:
#     validated = models.BooleanField(null=True, default=None)
#     # if the sample is in dataset (may have gold label
#     # which is not equal to predicton data)
#     in_dataset = models.BooleanField(null=True, default=False)
#
#
# class InputCase(models.Model):
#     # JSON Field?
#     input_data = models.CharField(max_length=200)

