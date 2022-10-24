import json
import os
import shutil
import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import ImportGoodsForm, DefaultSettingsForm, EmailForReportImport
from .models import DefaultSettings, File
from app_goods.models import Category, Product
from app_shops.models import Shop, ShopProduct

logger = logging.getLogger(__name__)


class AdminCustomSettings(View):

    @staticmethod
    def get(request):
        default_settings = DefaultSettings.objects.all()
        custom_settings_form = DefaultSettingsForm()
        if default_settings:
            custom_settings_form = DefaultSettingsForm(instance=default_settings[0])
        return render(request, template_name='admin/admin_custom_settings.html',
                      context={'custom_settings_form': custom_settings_form})

    @staticmethod
    def post(request):
        default_settings = DefaultSettings.objects.all()
        custom_settings_form = DefaultSettingsForm(request.POST)
        if default_settings:
            custom_settings_form = DefaultSettingsForm(request.POST, instance=default_settings[0])
        if custom_settings_form.is_valid():
            delivery_express_coast = custom_settings_form.cleaned_data.get('delivery_express_coast')
            min_order = custom_settings_form.cleaned_data.get('min_order')
            delivery_min = custom_settings_form.cleaned_data.get('delivery_min')

            if default_settings:
                default_settings[0].delivery_express_coast = delivery_express_coast
                default_settings[0].min_order = min_order
                default_settings[0].delivery_min = delivery_min
                default_settings[0].save()
            else:
                DefaultSettings.objects.create(delivery_express_coast=delivery_express_coast,
                                               min_order=min_order,
                                               delivery_min=delivery_min)
        else:
            messages.error(request, 'Error default settings. Bad values')
        messages.success(request, 'Default settings installed successfully')
        return redirect('/admin/')


class ImportGoodsView(View):

    @staticmethod
    def get(request):
        user = User.objects.get(id=request.user.id)
        file_form = ImportGoodsForm()
        email_form = EmailForReportImport()
        if request.user.email:
            email_form = EmailForReportImport(initial={'email': request.user.email}, instance=user)
        return render(request, 'admin/admin_import_goods.html', context={'file_form': file_form,
                                                                         'email_form': email_form})

    def post(self, request):
        log = ''
        user = User.objects.get(id=request.user.id)
        upload_file_form = ImportGoodsForm(request.POST, request.FILES)
        try:
            if upload_file_form.is_valid():
                files = request.FILES.getlist('file_field')
                for file in files:

                    try:
                        list_goods = json.loads(file.read().decode('utf-8'))

                        for product in list_goods.values():
                            name = product['name']
                            description = product['description']
                            quantity = product['quantity']
                            name_shop = product['shop']
                            name_category = product['category']
                            value_price = product['price']

                            shop = Shop.objects.get_or_create(name=name_shop, slug=name_shop)[0]
                            category = Category.objects.get_or_create(name=name_category, slug=name_category)[0]
                            try:
                                product = Product.objects.filter(name=name)
                                if product:
                                    shop_product = ShopProduct.objects.get(product=product[0])
                                    shop_product.quantity += quantity
                                    shop_product.save()
                                else:
                                    product = Product.objects.create(name=name, description=description, slug=name)
                                    product.category.add(category)
                                    product.save()
                                    ShopProduct.objects.create(shop=shop,
                                                               product=product,
                                                               price=value_price,
                                                               quantity=quantity)

                            except Exception as ex:
                                logger.error(f'import {file} error Bad values - {ex}')
                                log += f'import {file} error Bad values - {ex}\n'
                                messages.error(request, 'Error updating products. Bad values')

                        logger.info(f'import {file} - successfully')
                        log += f'import {file} - successfully\n'
                        messages.success(request, 'Products updated successfully')
                        self.save_file(request, shop, file)

                    except Exception as ex:
                        logger.error(f'import {file} error Bad file - {ex}')
                        log += f'import {file} error Bad file - {ex}\n'
                        messages.error(request, 'Error updating products. Bad file')
                        self.save_file(request, None, file)

        except Exception as ex:
            logger.error(f'import error load file - {ex}')
            log += f'import error load file - {ex}'
            messages.error(request, 'Error load file')

        email_form = EmailForReportImport(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data.get('email')
            self.send_message_for_admin(request, email, log)
        return redirect('/admin/')

    def save_file(self, request, shop, file):
        
        if shop:
            file_for_import = File.objects.create(file=file, shop=shop)
            if not os.path.exists(f'media/import/successful/shop_{shop.name}'):
                os.makedirs(f'media/import/successful/shop_{shop.name}')
            file_name = str(file_for_import.id) + '_' + file_for_import.file.name.split('import/')[-1]
            destination_path = os.path.abspath(f'{settings.MEDIA_ROOT}/import/successful/shop_{shop.name}/{file_name}')
        else:
            if not os.path.exists(f'media/import/unsuccessful'):
                os.makedirs(f'media/import/unsuccessful')
            file_for_import = File.objects.create(file=file)
            file_name = str(file_for_import.id) + '_' + file_for_import.file.name.split('import/')[-1]
            destination_path = os.path.abspath(f'{settings.MEDIA_ROOT}/import/unsuccessful/{file_name}')

        source_path = os.path.abspath(f'{settings.MEDIA_ROOT}/{file_for_import.file.name}')
        shutil.move(source_path, destination_path)

    @staticmethod
    def send_message_for_admin(request, email, log):
        try:
            send_mail("Report Import", log, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        except Exception as ex:
            logger.error(f'Failed message sending - {ex}')
            return HttpResponse('Failed message sending')
