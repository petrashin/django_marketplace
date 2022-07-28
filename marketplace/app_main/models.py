from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Role(models.Model):
    '''Роли пользователей'''
    name = models.CharField(verbose_name="Название роли", max_length=150)

    def __str__(self):
        return self.name


class Profile(models.Model):
    '''Профиль пользователя'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    avatar_url = models.CharField(max_length=256)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    role = models.ForeignKey(Role, verbose_name="Роль", on_delete=models.DO_NOTHING)
