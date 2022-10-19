from app_users.models import Profile


def compared_products(request):
    return {'number_of_compared_products': Profile().get_number_of_compared_products(request)}
