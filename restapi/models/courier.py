import datetime
from functools import reduce

from django.db import models
from django.contrib.postgres.fields import ArrayField

from restapi.models.order import *

class Courier(models.Model):
  FOOT = "foot"
  BIKE = "bike"
  CAR = "car"

  CATEGORY_CHOICES = [
    (FOOT, "Foot"),
    (BIKE, "Bike"),
    (CAR, "Car")
  ]

  identifier = models.IntegerField()
  category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
  regions = ArrayField(models.IntegerField())
  working_hours = ArrayField(models.CharField(max_length=25))

  def completed_orders(self):
    return Order.objects.filter(courier=self, status=Order.COMPLETED)

  def weight_capacity(self):
    if self.category == self.FOOT: return 10
    elif self.category == self.BIKE: return 15
    else: return 50

  def rating(self):
    orders_count = {}
    orders_avg_time = {}
    orders = self.completed_orders().order_by("completed_at")
    if len(orders) == 0: return None

    order = orders[0]
    region = order.region
    duration = (order.completed_at - order.assigned_at).total_seconds()

    if not region in orders_count:
      orders_count[region] = 0
      orders_avg_time[region] = 0

    orders_count[region] += 1
    orders_avg_time[region] += duration

    for i in range(1, len(orders)):
      order = orders[i]
      region = order.region
      duration = (order.completed_at - orders[i - 1].completed_at).total_seconds()
      if not region in orders_count:
        orders_count[region] = 0
        orders_avg_time[region] = 0

      orders_count[region] += 1
      orders_avg_time[region] += duration

    # import pdb; pdb.set_trace()

    for region in [*orders_count.keys()]:
      orders_avg_time[region] /= orders_count[region]

    min_duration = min(orders_avg_time.values())

    return round((3600 - min(min_duration, 3600)) / 3600 * 5, 2)

  def earnings(self):
    return reduce(
      lambda acc, order: acc + order.salary(),
      self.completed_orders(),
      0
    )

  def order_acceptance(self, order):
    #import pdb; pdb.set_trace()
    if order.region not in self.regions: return False
    if self.weight_capacity() < order.weight: return False
    if not self.__order_time_acceptance(order.delivery_hours): return False

    return True

  def __order_time_acceptance(self, delivery_hours):
    working_periods = list(map(self.__time_to_periods, self.working_hours))
    delivery_periods = list(map(self.__time_to_periods, delivery_hours))

    for working_period in working_periods:
      for delivery_period in delivery_periods:
        if working_period[0] > delivery_period[1]: continue
        if working_period[1] < delivery_period[0]: continue

        return True

    return False

  def __time_to_periods(self, time):
    start, end = time.split("-")

    return [self.__time_to_minutes(start), self.__time_to_minutes(end)]

  def __time_to_minutes(self, time):
    hours, minutes = list(map(int, time.split(":")))

    return hours * 60 + minutes

  def as_json(self):
    return {
      "courier_id": self.identifier,
      "courier_type": self.category,
      "regions": self.regions,
      "working_hours": self.working_hours
    }
