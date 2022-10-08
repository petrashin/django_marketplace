# Generated by Django 3.2.13 on 2022-10-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payment', '0002_auto_20220926_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paystatus',
            name='title',
            field=models.CharField(choices=[('1', 'Не оплачено'), ('2', 'Оплачено'), ('3', 'Ошибка оплаты - time_out'), ('4', 'Ошибка оплаты - err 35653'), ('5', 'Ошибка оплаты - err 999'), ('6', 'Ошибка - недостаточное кол-во товара')], default='Не оплачено', max_length=50, verbose_name='payment statuses'),
        ),
    ]
