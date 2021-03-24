import json

from django.http import HttpResponse
from django.views import View

from restapi.models import Order
import restapi.helpers as helpers

class OrderView(View):
  http_method_names = ["post"]

  def post(self, request):
    try:
      request_body = json.loads(request.body)
    except json.decoder.JSONDecodeError: return HttpResponse(status=400)

    invalid_entries_ids = self.__validate_post_request_body(request_body)
    if len(invalid_entries_ids) > 0: return helpers.render_http_400(invalid_entries_ids, "orders")

    created_entries_ids = []
    data = request_body["data"]
    for entry in data:
      order = Order(
        identifier=entry["order_id"],
        weight=entry["weight"],
        region=entry["region"],
        delivery_hours=entry["delivery_hours"]
      )
      order.save()

      created_entries_ids.append(order.identifier)

    return helpers.render_http_201(created_entries_ids, "orders")

  def __validate_post_request_body(self, request_body):
    def validate_weight(entry):
      if not "weight" in entry: return []

      if entry["weight"] > Order.MAX_ACCEPTABLE_WEIGHT or entry["weight"] < Order.MIN_ACCEPTABLE_WEIGHT:
        return [ { "attribute": "weight", "message": "invalid weight value" }]

      return []

    return helpers.validate_collection(
      request_body["data"],
      "order_id",
      required_attrs=["order_id", "weight", "region", "delivery_hours"],
      custom_validator=validate_weight
    )
