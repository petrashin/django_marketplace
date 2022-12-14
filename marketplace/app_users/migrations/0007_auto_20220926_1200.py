# Generated by Django 3.2.13 on 2022-09-26 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0008_auto_20220926_1200'),
        ('app_users', '0006_auto_20220910_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='compared_products',
            field=models.ManyToManyField(blank=True, related_name='compared_products', to='app_goods.Product'),
        ),
        migrations.AddField(
            model_name='role',
            name='name_en',
            field=models.CharField(max_length=150, null=True, verbose_name='role name'),
        ),
        migrations.AddField(
            model_name='role',
            name='name_ru',
            field=models.CharField(max_length=150, null=True, verbose_name='role name'),
        ),
        migrations.AlterField(
            model_name='image',
            name='avatar',
            field=models.ImageField(default='default.jpg', help_text="Field for saving the user's avatar", upload_to='avatars', verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='image',
            name='profile',
            field=models.OneToOneField(help_text='relationship with the Profile model', on_delete=django.db.models.deletion.CASCADE, to='app_users.profile', verbose_name='profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='balance'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='card',
            field=models.IntegerField(blank=True, null=True, verbose_name='card number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fullname',
            field=models.CharField(blank=True, max_length=256, verbose_name='fullname'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, verbose_name='phone_number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='published',
            field=models.BooleanField(default=True, verbose_name='published'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='recent_views',
            field=models.ManyToManyField(blank=True, related_name='recent_views', to='app_goods.Product'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_users.role', verbose_name='role'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=150, verbose_name='role name'),
        ),
        migrations.CreateModel(
            name='ComparedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_goods.product')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_users.profile')),
            ],
        ),
    ]
