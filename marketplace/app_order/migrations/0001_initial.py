# Generated by Django 3.2.13 on 2022-08-13 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('1', 'Доставка'), ('2', 'Экспресс-Доставка')], default='Доставка', max_length=30, verbose_name='вариант доставки')),
            ],
        ),
        migrations.CreateModel(
            name='PayMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('1', 'Онлайн картой'), ('2', 'Онлайн со случайного чужого счёта')], default='Онлайн картой', max_length=50, verbose_name='вариант оплаты')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_order', models.DateField(auto_now_add=True)),
                ('status_pay', models.BooleanField(default=False)),
                ('city', models.CharField(max_length=30, verbose_name='город')),
                ('address', models.CharField(max_length=100, verbose_name='адрес')),
                ('order_comment', models.CharField(blank=True, max_length=150, null=True, verbose_name='комментарий к заказу')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_order.delivery', verbose_name='вариант доставки')),
                ('pay_method', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app_order.paymethod', verbose_name='вариант оплаты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
