from app_goods.models import Category


def categories_processor(request):
    categories = {
        'categories': Category.objects.filter(parent_category__isnull=True)
    }
    return categories
