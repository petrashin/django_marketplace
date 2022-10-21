# Generated by Django 3.2.13 on 2022-10-20 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0009_auto_20221001_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_icon',
            field=models.FileField(default='E:\\icons\\categories\\test_category_icon.jpg', upload_to='icons/categories/', verbose_name='category icon'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount_name',
            field=models.CharField(blank=True, help_text='название скидки', max_length=50, verbose_name='discount_name'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount_name_en',
            field=models.CharField(blank=True, help_text='название скидки', max_length=50, null=True, verbose_name='discount_name'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount_name_ru',
            field=models.CharField(blank=True, help_text='название скидки', max_length=50, null=True, verbose_name='discount_name'),
        ),
    ]