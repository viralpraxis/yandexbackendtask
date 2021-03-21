import os, json
from datetime import datetime, timedelta

from django.test import TestCase, Client

from restapi.models import *

class GetCourier(TestCase):
  client = Client()
  current_time = datetime.datetime.utcnow()

  def setUp(self):
    courier = Courier(identifier=1, regions=[1, 2, 3], working_hours=["00:00-23:59"], category="bike")
    courier.save()

    orders = [
      Order(
        identifier=1, weight=10, region=1, delivery_hours=["10:00-11:00"], assigned_at=self.format_timedelta(170),
        courier=courier, status=Order.COMPLETED, completed_at=self.format_timedelta(110)
      ),
      Order(
        identifier=2, weight=10, region=2, delivery_hours=["10:00-11:00"], assigned_at=self.format_timedelta(125),
        courier=courier, status=Order.COMPLETED, completed_at=self.format_timedelta(80)
      ),
      Order(
        identifier=3, weight=10, region=3, delivery_hours=["10:00-11:00"], assigned_at=self.format_timedelta(100),
        courier=courier, status=Order.COMPLETED, completed_at=self.format_timedelta(50)
      ),
      Order(
        identifier=4, weight=10, region=1, delivery_hours=["10:00-11:00"], assigned_at=self.format_timedelta(60),
        courier=courier, status=Order.ASSIGNED
      )
    ]

    for order in orders: order.save()

  def test_renders_400_on_incorrect_courier_id(self):
    response = self.__do_request(2)

    self.assertEqual(response.status_code, 400)

  def test_renders_correct_response_on_correct_courier_id(self):
    response = self.__do_request(1)

    expected_response_body = {
      "courier_id": 1,
      "courier_type": "bike",
      "regions": [1, 2, 3],
      "working_hours": ["10:00-11:00"],
      "ratings": 2.50,
      "earnings": 13500
    }

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), expected_response_body)

  def __do_request(self, id):
    return self.client.get(f"/couriers/{id}")

  def format_timedelta(self, delta):
    return (self.current_time - timedelta(minutes=delta)).isoformat() + "Z"
