import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField

from restapi.models.courier import *

class Order(models.Model):
  MIN_ACCEPTABLE_WEIGHT = 0.01
  MAX_ACCEPTABLE_WEIGHT = 50
  DEFAULT_SALARY = 500

  PENDING = "PENDING"
  ASSIGNED = "ASSIGNED"
  COMPLETED = "COMPLETED"

  STATUS_CHOICES = [
    (PENDING, "Pending"),
    (ASSIGNED, "Assigned"),
    (COMPLETED, "Complited")
  ]

  identifier = models.IntegerField()
  courier = models.ForeignKey("Courier", null=True, on_delete=models.CASCADE)
  weight = models.FloatField()
  region = models.IntegerField()
  delivery_hours = ArrayField(models.CharField(max_length=25))
  status = models.CharField(max_length=25, null=True, choices=STATUS_CHOICES, default=PENDING)
  courier_category = models.CharField(max_length=25, null=True)
  assigned_at = models.DateTimeField(null=True)
  completed_at = models.DateTimeField(null=True)

  def salary(self):
    return self.DEFAULT_SALARY * self.salary_multiplier()

  def salary_multiplier(self):
    if self.courier_category == "foot": return 2
    elif self.courier_category == "bike": return 5
    else: return 9

  def assign_courier(self, courier):
    self.courier = courier
    self.courier_category = courier.category
    self.status = ASSIGNED
    self.assigned_at = datetime.datetime.utcnow().isoformat() + "Z"

    self.save()

  def unassign(self):
    self.courier = None
    self.courier_category = None
    self.status = PENDING
    self.assigned_at = None

    self.save()

  def complete(self, completed_at):
    self.status = COMPLETED
    self.completed_at = completed_at

    self.save()
