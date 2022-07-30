from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    avatar_url = models.CharField(max_length=256)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


class Reviews(models.Model):
    """ Отзывы """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    product = models.CharField(verbose_name="Товар", max_length=100, default=None)
    # TODO добавить связку с товаром

    def __str__(self):
        return self.user
