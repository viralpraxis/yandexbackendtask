import json
import os

from django.test import TestCase, Client

class PostCouriersTest(TestCase):
  client = Client()

  def test_renders_http_400_on_missing_entries_attributes(self):
    request_body = open(os.path.dirname(__file__) + "/fixtures/post_couriers_1.json").read()

    expected_response_body = {
      "validation_error": {
        "couriers": [
          {
            "id": 1,
            "errors": [
              {
                "attribute": "working_hours",
                "message": "missing required attribute"
              }
            ]
          },
          {
            "id": 3,
            "errors": [
              {
                "attribute": "courier_type",
                "message": "missing required attribute"
              }
            ]
          }
        ]
      }
    }

    response = self.__do_request(request_body)

    # import pdb; pdb.set_trace()
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.content), expected_response_body)

  def test_renders_http_400_on_any_additional_entries_attributes(self):
    request_body = open(os.path.dirname(__file__) + "/fixtures/post_couriers_2.json").read()

    expected_response_body = {
      "validation_error": {
        "couriers": [
          {
            "id": 3,
            "errors": [
              {
                "attribute": "additional_attribute",
                "message": "unexpected attribute"
              }
            ]
          }
        ]
      }
    }

    response = self.__do_request(request_body)

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.content), expected_response_body)

  def test_renders_correct_response_on_valid_request(self):
    request_body = open(os.path.dirname(__file__) + "/fixtures/post_couriers_3.json").read()

    expected_response_body = {
      "couriers": [{ "id": 1 }, { "id": 2 }, { "id": 3 }]
    }

    response = self.__do_request(request_body)

    self.assertEqual(response.status_code, 201)
    self.assertEqual(json.loads(response.content), expected_response_body)

  def __do_request(self, body):
    return self.client.post("/couriers", body, content_type="application/json")
