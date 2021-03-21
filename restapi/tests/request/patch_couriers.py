import json
import os

from django.test import TestCase, Client

from restapi.models import *

class PatchCouriersTest(TestCase):
  client = Client()

  def setUp(self):
    courier = Courier(identifier=1, category="car", regions=[1, 2, 3], working_hours=["10:00-12:00", "14:01-14-02"])
    courier.save()

    orders = [
      Order(identifier=1, weight=10, region=1, delivery_hours=["10:00-11:00", "14:10-15:00"], courier=courier, status=Order.ASSIGNED),
      Order(identifier=2, weight=12, region=2, delivery_hours=["10:00-11:00", "14:10-15:00"], courier=courier, status=Order.ASSIGNED),
      Order(identifier=3, weight=45, region=3, delivery_hours=["10:00-11:00", "14:10-15:00"], courier=courier, status=Order.ASSIGNED),
      Order(identifier=4, weight=10, region=3, delivery_hours=["03:00-04:00", "14:01-14:02"])
    ]

    for order in orders: order.save()

  def test_marks_rrders_as_unassigned_if_required(self):
    request_body = open(os.path.dirname(__file__) + "/fixtures/patch_couriers_1.json").read()
    response = self.__do_request(request_body)

    expected_response_body = {
      "courier_id": 1,
      "courier_type": "foot",
      "regions": [2, 3, 4],
      "working_hours": ["10:00-12:00", "14:01-14-02"]
    }

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), expected_response_body)
    self.assertEqual(Order.objects.get(identifier=3).courier, None)

  def __do_request(self, request_body, courier_id=1):
    return self.client.patch(
      f"/couriers/{courier_id}",
      request_body,
      content_type="application/json"
    )
