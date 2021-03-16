from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from restapi.models import Courier

import json

@require_http_methods(["POST"])
def create(request):
  parsed_request_body = json.loads(request.body)
  failed_validation_entries_ids = validate_request_body(parsed_request_body)

  # fix format
  if len(failed_validation_entries_ids) > 0:
    return render_http_400(failed_validation_entries_ids)

  created_entries_ids = []
  data = parsed_request_body["data"]
  for entry in data:
    courier = Courier(
      identifier=entry["courier_id"],
      category=entry["courier_type"],
      regions=entry["regions"],
      working_hours=entry["working_hours"]
    )
    courier.save()

    created_entries_ids.append(courier.id)

  return HttpResponse(
    json.dumps(created_entries_ids),
    content_type="application/json",
    status=201
  )


def validate_request_body(body):
  failed_validation_entries_ids = []

  for entry in body["data"]:
    if list(entry.keys()) != ['courier_id', 'courier_type', 'regions', 'working_hours']:
      failed_validation_entries_ids.append(entry["courier_id"])

  return failed_validation_entries_ids

def render_http_400(failed_validation_entries_ids):
  body = {
    "validation_error": {
      "couriers": list(map(lambda x : { "id": x }, failed_validation_entries_ids))
    }
  }

  return HttpResponse(
    json.dumps(body),
    content_type="application/json",
    status=400
  )
