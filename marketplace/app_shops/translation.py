from modeltranslation.translator import register, TranslationOptions
from .models import Shop


@register(Shop)
class ShopTranslationOptions(TranslationOptions):
    fields = ('name', 'about', 'country', 'city', 'street')

