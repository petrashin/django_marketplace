# Generated by Django 3.2.13 on 2022-08-08 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='наименование')),
                ('slug', models.SlugField(help_text='уникальный фрагмент url на основе наименования магазина', max_length=255, verbose_name='url')),
            ],
            options={
                'verbose_name': 'магазин',
                'verbose_name_plural': 'магазины',
                'db_table': 'shops',
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(verbose_name='количество')),
                ('price', models.ForeignKey(help_text='связь с моделью Price', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_products', to='app_goods.price', verbose_name='цена')),
                ('product', models.ForeignKey(help_text='связь с моделью Product', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_products', to='app_goods.product', verbose_name='товар')),
                ('shop', models.ForeignKey(help_text='связь с моделью Shop', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_products', to='app_shops.shop', verbose_name='магазин')),
            ],
        ),
    ]
