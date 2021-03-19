import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render

from restapi.models import Courier, Order
import restapi.helpers as helpers

class OrdersCompletionView(View):
  http_methods_allowed = ['post']

  def post(self, request):
    request_body = json.loads(request.body)

    if not self.__validate_post_request_body: return HttpResponse(status=400)

    courier = self.__find_courier(request_body['courier_id'])
    order = self.__find_order(request_body['order_id'])

    if not(courier) or not(order) or order.status == "PENDING" or order.courier.identifier != courier.identifier:
      return HttpResponse(status=400)

    order.complete(request_body['complete_time'])

    return JsonResponse({ "order_id": order.identifier })

  def __find_courier(self, id):
    try:
      return Courier.objects.get(identifier=id)
    except Courier.DoesNotExist:
      pass

  def __find_order(self, id):
    try:
      return Order.objects.get(identifier=id)
    except Order.DoesNotExist:
      pass

  def __validate_post_request_body(self, request_body):
    return list(request_body.keys()) == ['courier_id', 'order_id', 'complete_time']
