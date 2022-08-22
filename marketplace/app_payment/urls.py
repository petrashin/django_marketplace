from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import AddOrder, Test

urlpatterns = {
    path('', AddOrder.as_view(), name='payment'),
    path('api-auth/', include('rest_framework.urls')),
    path('test_payment/', Test.as_view(), name='test'),
}
urlpatterns = format_suffix_patterns(urlpatterns)
