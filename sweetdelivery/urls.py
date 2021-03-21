from django.urls import include, path

from restapi.views import *

urlpatterns = [
    path('', include('restapi.urls'))
]
