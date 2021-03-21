import json, os

from django.test import TestCase, Client

from restapi.models import *

class PostOrdersCompleteTest(TestCase):
  client = Client()

  def setUp(self):
    target_courier = Courier(identifier=1, category="bike", regions=[1, 2, 10], working_hours=["08:10-12:10", "14:59-15:20"])
    decoy_courier = Courier(identifier=2, category="foot", regions=[7, 200], working_hours=["10:20-10:21", "15:59-23:20"])
    couriers = [target_courier, decoy_courier]

    orders = [
      Order(identifier=1, weight=10, region=1, delivery_hours=["10:00-11:00", "14:10-15:00"], status="ASSIGNED", courier=target_courier),
      Order(identifier=2, weight=12, region=1, delivery_hours=["10:00-11:00", "14:10-15:00"], status="COMPLETED", courier=target_courier),
      Order(identifier=3, weight=100, region=1, delivery_hours=["10:00-11:00", "14:10-15:00"], status="ASSIGNED", courier=decoy_courier),
      Order(identifier=4, weight=100, region=1, delivery_hours=["10:00-11:00", "14:10-15:00"], status="PENDING"),
    ]

    for entry in [*couriers, *orders]: entry.save()

  def test_renders_http_400_for_pending_order(self):
    request_body = open(os.path.dirname(__file__) + '/fixtures/post_orders_complete_1.json').read()
    response = self.__do_request(request_body)

    self.assertEqual(response.status_code, 400)

  def test_renders_order_id_for_completed_by_target_courier_order(self):
    request_body = open(os.path.dirname(__file__) + '/fixtures/post_orders_complete_2.json').read()
    response = self.__do_request(request_body)

    expected_response_body = {
      "order_id": 2
    }

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), expected_response_body)

  def test_renders_order_id_and_completes_assigned_to_target_courier_order(self):
    request_body = open(os.path.dirname(__file__) + '/fixtures/post_orders_complete_3.json').read()
    response = self.__do_request(request_body)

    expected_response_body = {
      "order_id": 1
    }

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), expected_response_body)
    self.assertTrue(Order.objects.get(identifier=1).completed_at is not None)

  def test_renders_http_400_for_assigned_to_decoy_courier_order(self):
    request_body = open(os.path.dirname(__file__) + '/fixtures/post_orders_complete_4.json').read()
    response = self.__do_request(request_body)

    self.assertEqual(response.status_code, 400)

  def __do_request(self, request_body):
    return self.client.post("/orders/complete", request_body, content_type="application/json")
