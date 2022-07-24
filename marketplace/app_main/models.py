from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    avatar_url = models.CharField(max_length=256)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    