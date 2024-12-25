from django.urls import path
from . import api
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', api.nlp_list, name='nlp_list'),
    path('create/', api.nlp_create, name='nlp_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
