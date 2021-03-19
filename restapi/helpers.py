from django.http import JsonResponse

def render_http_400(invalid_entries_ids, root_key):
  response_body = {
    "validation_error": {
      root_key: format_id_array(invalid_entries_ids)
    }
  }

  return JsonResponse(response_body, status=400)

def render_http_201(created_entries_ids, root_key):
  response_body = {
    root_key: format_id_array(created_entries_ids)
  }

  return JsonResponse(response_body, status=201)

def format_id_array(entries_ids):
  return list(map(lambda x : { "id": x }, entries_ids))
