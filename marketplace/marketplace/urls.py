from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from custom_admin.views import ImportGoodsView, AdminCustomSettings
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/custom_settings/', AdminCustomSettings.as_view(), name='admin_custom_settings'),
    path('admin/import_goods/', ImportGoodsView.as_view(), name='admin_import_goods'),
    path('admin/', admin.site.urls),

] + i18n_patterns(
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('cart/', include('cart.urls')),
    path('auth/', include('app_auth.urls')),
    path('', include('app_users.urls')),
    path('', include('app_shops.urls')),
    path('', include('app_goods.urls')),
    path('account/', include('app_account.urls')),
    path('', include('app_order.urls')),
    path('api/', include('app_payment.urls')),
    prefix_default_language=False
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
