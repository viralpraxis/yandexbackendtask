from django.http import JsonResponse

def render_http_400(validation_result, root_key=None):
  response_body = {
    "validation_error": {
      root_key: validation_result
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

# well i could use jsonschema but its API is too ugly thus i
# decided to write my own naive implementation without type checking
# ¯\_( ͡° ͜ʖ ͡°)_/¯

def validate_collection(entries, id_key, required_attrs=[], allowed_attrs=None, custom_validator=None):
  if allowed_attrs is None: allowed_attrs = required_attrs

  collection_validation_result = []

  for entry in entries:
    entry_errors = validate_entry(entry, required_attrs, allowed_attrs)
    if custom_validator:
      entry_errors += custom_validator(entry)

    if len(entry_errors):
      entry_validation_result = {}
      entry_validation_result["id"] = entry[id_key]
      entry_validation_result["errors"] = entry_errors

      collection_validation_result.append(entry_validation_result)

  return collection_validation_result

def validate_entry(entry, required_attrs=[], allowed_attrs=[]):
  errors = []
  attrs = list(entry.keys())

  missed_attrs = list(set(required_attrs) - set(attrs))
  for missed_attr in missed_attrs:
    errors.append(
      {
        "attribute": missed_attr,
        "message": "missing required attribute"
      }
    )

  unexpected_attrs = list(set(attrs) - set(allowed_attrs))
  for unexpected_attr in unexpected_attrs:
    errors.append(
      {
        "attribute": unexpected_attr,
        "message": "unexpected attribute"
      }
    )

  return errors
