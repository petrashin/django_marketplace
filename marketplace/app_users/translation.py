from modeltranslation.translator import register, TranslationOptions
from .models import Role, Profile, Image


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('user', 'phone_number', 'balance', 'role', 'published')


@register(Role)
class RoleTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Image)
class ImageTranslationOptions(TranslationOptions):
    fields = ('profile', 'avatar')


