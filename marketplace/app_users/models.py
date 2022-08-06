from django.contrib.auth.models import User
from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=25)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING, related_name="sub")
    category_icon = models.FileField(upload_to='static/assets/img/icons/departments/')

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.user


class Image(models.Model):
    """Модель изображения аватарки"""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name='профиль',
                                   help_text='Связь с моделью профиля пользователя')
    avatar = models.ImageField(upload_to='avatars', verbose_name='аватарка',
                               help_text='Поле для сохранения аватарки пользователя')
