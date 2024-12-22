from django.urls import path
from . import api


urlpatterns = [
    path('', api.nlp_list, name='nlp_list'),
    path('create/', api.nlp_create, name='nlp_create'),
]
