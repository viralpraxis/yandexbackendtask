from django.db import models
from django.contrib.postgres.fields import ArrayField

class Order(models.Model):
  MIN_ACCEPTABLE_WEIGHT = 0.01
  MAX_ACCEPTABLE_WEIGHT = 50

  PENDING = "PENDING"
  ASSIGNED = "ASSIGNED"
  COMPLETED = "COMPLETED"

  STATUS_CHOICES = [
    (PENDING, "Pending"),
    (ASSIGNED, "Assigned"),
    (COMPLETED, "Complted")
  ]

  courier = models.ForeignKey('Courier', null=True, on_delete=models.CASCADE)
  identifier = models.IntegerField()
  weight = models.FloatField()
  region = models.IntegerField()
  delivery_hours = ArrayField(models.CharField(max_length=25))
  status = models.CharField(
    max_length=25,
    null=True,
    choices=STATUS_CHOICES,
    default=PENDING
   )
  completed_at = models.CharField(max_length=50, null=True)
