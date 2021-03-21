import json, datetime

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render

from restapi.models import Courier, Order
import restapi.helpers as helpers

class OrdersAssignmentView(View):
  http_method_names = ["post"]

  def post(self, request, *args, **kwargs):
    parsed_request_body = json.loads(request.body)

    courier = self.__find_courier(parsed_request_body["courier_id"])
    if not(courier): return HttpResponse(status=400)

    orders = Order.objects.filter(status=Order.PENDING)

    # TODO: transaction wrapper
    assigned_orders_ids = []
    for order in orders:
      if courier.order_acceptance(order):
        assigned_orders_ids.append(order.identifier)
        order.assign_courier(courier)

    return self.__render_http_200(assigned_orders_ids)

  def __render_http_200(self, orders_ids):
    # TODO: RFC 3339
    response_body = {
      "orders": helpers.format_id_array(orders_ids),
      "assign_time": datetime.datetime.now().isoformat() + "Z"
    }

    return JsonResponse(response_body)

  def __find_courier(self, courier_id):
    try:
      return Courier.objects.get(identifier=courier_id)
    except Courier.DoesNotExist:
      pass
