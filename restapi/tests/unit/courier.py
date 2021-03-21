from datetime import datetime, timedelta

from django.test import TestCase, Client

from restapi.models import *

class CourierTest(TestCase):
  current_time = datetime.datetime.utcnow()

  def setUp(self):
    courier = Courier(identifier=1, regions=[1, 2, 3], working_hours=['00:00-23:59'], category='bike')
    courier.save()

    orders = [
      Order(
        identifier=1, weight=10, region=1, delivery_hours=['10:00-11:00'], assigned_at=self.format_timedelta(170),
        courier=courier, status=Order.COMPLETED, completed_at=self.format_timedelta(110)
      ),
      Order(
        identifier=2, weight=10, region=2, delivery_hours=['10:00-11:00'], assigned_at=self.format_timedelta(125),
        courier=courier, status=Order.COMPLETED, completed_at=self.format_timedelta(80)
      ),
      Order(
        identifier=3, weight=10, region=3, delivery_hours=['10:00-11:00'], assigned_at=self.format_timedelta(100),
        courier=courier, status=Order.COMPLETED, completed_at=self.format_timedelta(50)
      ),
      Order(
        identifier=4, weight=10, region=1, delivery_hours=['10:00-11:00'], assigned_at=self.format_timedelta(60),
        courier=courier, status=Order.ASSIGNED
      )
    ]

    for order in orders: order.save()

  def test_courier_has_correct_rating(self):
    courier = Courier.objects.get(identifier=1)

    self.assertEqual(courier.rating(), '2.50')

  def test_courier_has_correct_earnings(self):
    courier = Courier.objects.get(identifier=1)

    self.assertEqual(courier.earnings(), 13500)

  def format_timedelta(self, delta):
    return (self.current_time - timedelta(minutes=delta)).isoformat() + "Z"
