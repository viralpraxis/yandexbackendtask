import os, json

from django.test import TestCase, Client

from restapi.models import *

class PostOrdersTest(TestCase):
  client = Client()

  def test_renders_http_400_on_missing_attributes(self):
    request_body = open(os.path.dirname(__file__) + "/fixtures/post_orders_1.json").read()
    response = self.__do_request(request_body)

    expected_response_body = {
      "validation_error": {
        "orders": [
          {
            "id": 2,
            "errors": [
              {
                "attribute": "weight",
                "message": "missing required attribute"
              }
            ]
          },
          {
            "id": 3,
            "errors": [
              {
                "attribute": "weight",
                "message": "invalid weight value"
              }
            ]
          }
        ]
      }
    }

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.content), expected_response_body)

  def test_renders_http_400_on_unexpected_attributes(self):
    request_body = open(os.path.dirname(__file__) + "/fixtures/post_orders_2.json").read()
    response = self.__do_request(request_body)

    expected_response_body = {
      "validation_error": {
        "orders": [
          { 
            "id": 1,
            "errors": [
              {
                "attribute": "sex",
                "message": "unexpected attribute"
              }
            ]
          }
        ]
      }
    }

    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.content), expected_response_body)

  def test_renders_http_201_with_correct_body_on_correct_response(self):
    request_body = open(os.path.dirname(__file__) + "/fixtures/post_orders_3.json").read()
    response = self.__do_request(request_body)

    expected_response_body = {
      "orders": [{ "id": 1 }, { "id": 2, }, { "id": 3 }]
    }

    self.assertEqual(response.status_code, 201)
    self.assertEqual(json.loads(response.content), expected_response_body)

  def __do_request(self, body):
    return self.client.post("/orders", body, content_type="application/json")
