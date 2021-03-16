from django.db import models

from django.contrib.postgres.fields import ArrayField

class Courier(models.Model):
  identifier = models.IntegerField()
  category = models.CharField(max_length=10)
  regions = ArrayField(models.IntegerField())
  working_hours = ArrayField(models.CharField(max_length=25))
