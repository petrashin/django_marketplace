from django.contrib.auth.models import User
from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=25)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING, related_name="sub")
    category_icon = models.FileField(upload_to='static/assets/img/icons/departments/')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    avatar_url = models.CharField(max_length=256)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user


class Reviews(models.Model):
    """ Отзывы """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    product = models.CharField(verbose_name="Товар", max_length=100, default=None)

    # TODO добавить связку с товаром

    def __str__(self):
        return self.user
