# Generated by Django 3.2.13 on 2022-09-16 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cartitems_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='published',
            field=models.BooleanField(default=True, verbose_name='опубликовать'),
        ),
    ]