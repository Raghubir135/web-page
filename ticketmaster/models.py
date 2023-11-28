from django.db import models


# Create your models here.
class Entry(models.Model):
    events = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
