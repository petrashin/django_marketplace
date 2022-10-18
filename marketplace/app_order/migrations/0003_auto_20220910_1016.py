# Generated by Django 3.2.13 on 2022-09-10 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0002_auto_20220825_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app_order.paymethod', verbose_name='вариант оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_error',
            field=models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='текст ошибки, возникшей при оплате'),
        ),
    ]
