from modeltranslation.translator import register, TranslationOptions
from .models import Discount, Category, Product, Reviews


@register(Discount)
class DiscountTranslationOptions(TranslationOptions):
    fields = ('discount_type', 'description')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'parent_category')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Reviews)
class ReviewsTranslationOptions(TranslationOptions):
    fields = ('text',)
