from django.urls import path
from ic_dataset import views
# from rest_framework.urlpatterns import format_suffix_patterns
app_name = 'ic_dataset'

urlpatterns = [
    path('download_intent_phrases', views.download_intent_phrases, name='download_intent_phrases'),
    # path('ic_dataset/upload_intents_json', views.upload_intents_json_view, name='upload_intents_json_view'),
    path('upload_intents_json', views.upload_intents_json_view, name='upload_intents_json_view'),
    path('train_model_view', views.train_model_view, name='train_model_view'),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
