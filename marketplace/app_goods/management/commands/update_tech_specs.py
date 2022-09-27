from random import choice
from app_goods.models import Product
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        list_random_speech = ['privet', 'poka', 'kak dela?']
        prod_list = list()
        for i in products:
            test = choice(list_random_speech)
            i.technical_specs = {'size': test}
            prod_list.append(i)

        Product.objects.bulk_update(prod_list, fields=['technical_specs'])
