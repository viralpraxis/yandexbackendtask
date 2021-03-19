import json

from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

from restapi.models import Courier, Order
import restapi.helpers as helpers

class OrdersAssignmentView(View):
  http_methods_allowed = ['post']

  def post(self, request, *args, **kwargs):
    courier = self.__find_courier(kwargs['courier_id'])
    if not(courier): return HttpResponse(status=400)

    orders = Order.objects.filter(status='pending')
    orders = filter(courier.order_acceptance, orders)

    # TODO: wrap via transaction
    orders.update(courier=courier, status=Order.ASSIGNED)

    return self.__render_http_200(orders)

  def __render_http_200(self, orders):
    orders_ids = list(map(lambda x : { "id": x }, orders))
    # TODO: RFC 3339
    response_body = {
      "orders": orders_ids,
      "assign_time": "TIME PLACEHOLDER"
    }

    return HttpResponse(
      response_body,
      content_type="application/json",
      status=200
    )

  def __find_courier(self, courier_id):
    try:
      return Courier.objects.get(identifier=courier_id)
    except Courier.DoesNotExist:
      pass
