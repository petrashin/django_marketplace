# Generated by Django 3.2.13 on 2022-09-19 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0008_auto_20220926_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_icon',
            field=models.FileField(default='C:\\Users\\kulikov.a\\PycharmProjects\\python_django_group_diploma\\marketplace\\media\\icons\\categories\\test_category_icon.jpg', upload_to='icons/categories/', verbose_name='иконка категории'),
        ),
    ]
