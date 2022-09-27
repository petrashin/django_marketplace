import random
from random import choice, randint, sample
from app_goods.models import Product
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """
        1. Рандомно определяется количество характеристик, которое будет добавлено
        2. Рандомно выбирается данное количество характеристик из random_specs.keys()
        3. Рандомно выбирается одно значение из списка random_specs['key']
        4. Изменный товар добавляется в список для обновления
        """

        random_specs = {
            'size': ['big', 'small', 'medium', 'large'],
            'rating': [0, 1, 2, 3, 4, 5],
            'diagonal': [6.1, 6.2, 7.5, 10.8, 13.7],
            'screen_freq': [60, 75, 120, 144, 240],
            'country': ['Russia', 'USA', 'China', 'India'],
            'guarantee': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'power': [100, 200, 300, 400]
        }

        products = Product.objects.all()
        updated_products = []

        for product in products:
            num_of_specs = randint(1, len(random_specs))
            specs = random.sample(random_specs.keys(), num_of_specs)
            specs_result = {}
            for spec in specs:
                specs_result[spec] = choice(random_specs[spec])
            product.technical_specs = specs_result
            updated_products.append(product)

        Product.objects.bulk_update(updated_products, fields=['technical_specs'])
