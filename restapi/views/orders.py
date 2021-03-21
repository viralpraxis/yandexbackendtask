import json

from django.http import HttpResponse
from django.views import View

from restapi.models import Order
import restapi.helpers as helpers

class OrderView(View):
  http_methods_allowed = ["post"]

  def post(self, request):
    parsed_request_body = json.loads(request.body)

    invalid_entries_ids = self.__validate_post_request_body(parsed_request_body)
    if len(invalid_entries_ids) > 0: return helpers.render_http_400(invalid_entries_ids, "orders")

    created_entries_ids = []
    data = parsed_request_body["data"]
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
    invalid_entries_ids = []

    for entry in request_body["data"]:
      if not self.__ensure_entry_validity(entry):
        invalid_entries_ids.append(entry["order_id"])

    return invalid_entries_ids

  def __ensure_entry_validity(self, entry):
    entry_fields = ["order_id", "weight", "region", "delivery_hours"]

    if list(entry.keys()) != entry_fields: return False
    if entry["weight"] > Order.MAX_ACCEPTABLE_WEIGHT or entry["weight"] < Order.MIN_ACCEPTABLE_WEIGHT:
      return False

    return True

