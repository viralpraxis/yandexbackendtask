import os, json

from django.test import TestCase, Client

from restapi.models import *

class PostOrdersAssignTest(TestCase):
  client = Client()

  def setUp(self):
    orders = [
      Order(identifier=1, weight=10, region=1, delivery_hours=["10:00-11:00", "14:10-15:00"]),
      Order(identifier=2, weight=12, region=1, delivery_hours=["10:00-11:00", "14:10-15:00"]),
      Order(identifier=3, weight=100, region=1, delivery_hours=["10:00-11:00", "14:10-15:00"]),
      Order(identifier=4, weight=1000.50, region=2, delivery_hours=["10:00-11:00", "14:10-15:00"]),
      Order(identifier=5, weight=1, region=2, delivery_hours=["10:00-11:00", "14:10-15:00"], status="ASSIGNED"),
      Order(identifier=10, weight=20, region=2, delivery_hours=["10:00-11:00", "14:10-15:00"]),
      Order(identifier=20, weight=15, region=3, delivery_hours=["10:00-11:00", "14:10-15:00"]),
      Order(identifier=21, weight=1.05, region=3, delivery_hours=["10:00-11:00", "14:10-15:00"]),
      Order(identifier=25, weight=0.01, region=3, delivery_hours=["10:00-11:00", "14:10-15:00"]),
      Order(identifier=100, weight=0.02, region=10, delivery_hours=["10:00-11:00", "14:10-15:00"]),
    ]
    couriers = [
      Courier(identifier=1, category="bike", regions=[1, 2, 10], working_hours=["08:10-12:10", "14:59-15:20"]),
      Courier(identifier=2, category="foot", regions=[7, 200], working_hours=["10:20-10:21", "15:59-23:20"])
    ]

    for entry in [*orders, *couriers]: entry.save()

  def test_renders_http_400_on_missing_courier_entry(self):
    response = self.__do_request(json.dumps({ "courier_id": 239 }))

    self.assertEqual(response.status_code, 400)

  def test_renders_correct_response_on_valid_request(self):
    response = self.__do_request({ "courier_id": 1 })
    response_body = json.loads(response.content)

    self.assertTrue("assign_time" in response_body)
    self.assertEqual(response_body["orders"], [{ "id": 1 }, { "id": 2 }, { "id": 100 }])
    self.assertEqual(response.status_code, 200)

  def test_renders_empty_array_if_required(self):
    response = self.__do_request({ "courier_id": 2 })
    response_body = json.loads(response.content)

    self.assertTrue("assign_time" in response_body)
    self.assertEqual(response_body["orders"], [])
    self.assertEqual(response.status_code, 200)

  def __do_request(self, request_body):
    return self.client.post("/orders/assign", request_body, content_type="application/json")

