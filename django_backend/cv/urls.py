from django.urls import path
from . import api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', api.cv_list, name='cv_list'),
    path('create/', api.cv_create, name='cv_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)