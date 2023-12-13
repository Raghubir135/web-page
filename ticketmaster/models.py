# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    # User model is created by Django. Instead of creating our own User model, we can simply use Django's user model.
    # the following line create a ForeignKey in your table
    # Since each user can have many comments, 1-to-many relationship is needed.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    eventID = models.CharField(max_length=20, blank=True, null=True)

