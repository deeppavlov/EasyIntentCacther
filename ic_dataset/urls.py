from django.urls import path
from ic_dataset import views
# from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('ic_dataset/download_intent_phrases', views.download_intent_phrases, name='download_intent_phrases'),
    path('ic_dataset/upload_intents_json', views.upload_intents_json_view, name='upload_intents_json_view'),
    path('ic_dataset/train_model_view', views.train_model_view, name='train_model_view'),
    # path('ner_dataset/training_samples/<int:pk>/', views.training_sample_detail),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
