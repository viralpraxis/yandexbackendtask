import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from restapi.models import Courier

class ShowCourierView(View):
  http_method_names = ["get"]

  def get(self, request, *args, **kwargs):
    courier = self.__find_courier(kwargs["id"])
    if not(courier): return HttpResponse(status_code=400)

    response_body = {
      "courier_id": courier.identifier,
      "courier_type": courier.category,
      "regions": courier.regions,
      "working_hours": courier.working_hours,
      "rating": courier.rating,
      "earnings": courier.earnings
    }

    return JsonResponse(response_body)

  def __find_courier(self, id):
    try:
      return Courier.objects.get(identifier=id)
    except Courier.DoesNotExist:
      pass
