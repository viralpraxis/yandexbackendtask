from django.contrib import admin
from django.urls import path

from restapi import views as restapi_views

urlpatterns = [
    path("couriers", restapi_views.create)
]
