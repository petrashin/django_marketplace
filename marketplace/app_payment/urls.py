from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import OrderPayment

urlpatterns = {
    path('', OrderPayment.as_view(), name='payment'),
    path('api-auth/', include('rest_framework.urls')),
}
urlpatterns = format_suffix_patterns(urlpatterns)
