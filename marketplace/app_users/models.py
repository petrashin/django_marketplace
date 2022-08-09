from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    """Роли пользователей"""
    name = models.CharField(verbose_name="Название роли", max_length=150)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    role = models.OneToOneField(Role, verbose_name="Роль", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Image(models.Model):
    """Модель изображения аватарки"""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name='профиль',
                                   help_text='Связь с моделью профиля пользователя')
    avatar = models.ImageField(upload_to='avatars', verbose_name='аватарка',
                               help_text='Поле для сохранения аватарки пользователя')
