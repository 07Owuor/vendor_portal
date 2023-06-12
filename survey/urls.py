from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_home, name='survey_home')
]
