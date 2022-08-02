# Generated by Django 3.2.13 on 2022-07-28 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0005_auto_20220728_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_type',
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.ForeignKey(help_text='связь с моделью Price', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app_goods.price', verbose_name='цена'),
        ),
    ]
