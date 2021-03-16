from django.test import TestCase, Client

import json

class BasicTest(TestCase):
  client = Client()

  def test_renders_http_400_on_missing_entries_attributes(self):
    request_body = {
      "data": [
        {
          "courier_id": 1,
          "courier_type": "foot",
          "regions": [1337, 420, 42],
        },
        {
          "courier_id": 2,
          "courier_type": "bike",
          "regions": [1337, 420, 42],
          "working_hours": ["10:20-20:20"]
        },
        {
          "courier_id": 3
        }
      ]
    }

    expected_response_body = {
      "validation_error": {
        "couriers": [{ "id": 1 }, { "id": 3}]
      }
    }

    response = self.client.post("/couriers", request_body, content_type="application/json")

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.content), expected_response_body)

