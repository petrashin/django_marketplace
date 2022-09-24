from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from app_goods.models import Product
from django.db import models


class Role(models.Model):
    """Роли пользователей"""
    name = models.CharField(verbose_name=_("role name"), max_length=150)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(verbose_name=_('phone_number'), max_length=12, blank=True)
    balance = models.DecimalField(verbose_name=_('balance'), max_digits=10, decimal_places=2, default=0)
    role = models.ForeignKey(Role, verbose_name=_('role'), on_delete=models.PROTECT)
    fullname = models.CharField(max_length=256, verbose_name=_('fullname'), blank=True)
    published = models.BooleanField(default=True, verbose_name=_('published'))
    card = models.IntegerField(verbose_name=_('card number'), blank=True, null=True)
    recent_views = models.ManyToManyField(Product, blank=True, related_name='recent_views')
    compared_products = models.ManyToManyField(Product, blank=True, related_name='compared_products')

    def __str__(self):
        return self.user.get_full_name()


class Image(models.Model):
    """Модель изображения аватарки"""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name=_('profile'),
                                   help_text=_('relationship with the Profile model'))
    avatar = models.ImageField(upload_to='avatars', verbose_name=_('avatar'),
                               help_text=_("Field for saving the user's avatar"),
                               default='default.jpg')


class ViewsHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, default=None)
    viewed_at = models.DateTimeField(auto_now_add=True)


class ComparedProducts(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, default=None)
    added_at = models.DateTimeField(auto_now_add=True)
