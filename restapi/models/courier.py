from django.db import models
from django.contrib.postgres.fields import ArrayField

class Courier(models.Model):
  identifier = models.IntegerField()
  category = models.CharField(max_length=10)
  regions = ArrayField(models.IntegerField())
  working_hours = ArrayField(models.CharField(max_length=25))

  def weight_capacity(self):
    if self.category == "foot":
      return 10
    elif self.category == "bike":
      return 15
    else:
      return 50

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
