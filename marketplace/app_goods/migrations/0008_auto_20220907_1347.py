# Generated by Django 3.2.13 on 2022-09-07 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0007_merge_20220907_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='limited_edition',
            field=models.BooleanField(default=False, verbose_name='ограниченный выпуск'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_icon',
            field=models.FileField(default='C:\\Users\\Аня\\PycharmProjects\\python_django_group_diploma\\marketplace\\media\\icons\\categories\\test_category_icon.jpg', upload_to='icons/categories/', verbose_name='иконка категории'),
        ),
    ]
