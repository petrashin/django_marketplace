from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Расширение модели пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь', help_text='Связь с моделью пользователя')
    phone_number = models.CharField(max_length=12, verbose_name='номер телефона', help_text='Номер телефона пользователя максимальной длиной в 12 символов')
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='баланс', help_text='Баланс пользователя, максимально возможное число: 99999999.99')


class Image(models.Model):
    """Модель изображения аватарки"""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name='профиль', help_text='Связь с моделью профиля пользователя')
    avatar = models.ImageField(upload_to='avatars', verbose_name='аватарка', help_text='Поле для сохранения аватарки пользователя')