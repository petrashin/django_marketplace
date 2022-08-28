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
    phone_number = models.CharField(verbose_name="Телефон", max_length=12, blank=True)
    balance = models.DecimalField(verbose_name="Баланс", max_digits=10, decimal_places=2, default=0)
    role = models.ForeignKey(Role, verbose_name="Роль", on_delete=models.PROTECT)
    fullname = models.CharField(max_length=256, verbose_name="ФИО", blank=True)
    published = models.BooleanField(default=True, verbose_name='опубликовать')

    def __str__(self):
        return self.user.get_full_name()


class Image(models.Model):
    """Модель изображения аватарки"""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name='профиль',
                                   help_text='Связь с моделью профиля пользователя')
    avatar = models.ImageField(upload_to='avatars', verbose_name='аватарка',
                               help_text='Поле для сохранения аватарки пользователя',
                               default='default.jpg')
