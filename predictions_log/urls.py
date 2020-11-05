from django.urls import path
from predictions_log import views

urlpatterns = [
    path('predict/', views.ic_predict),
]
