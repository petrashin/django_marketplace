import random

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import PayStatus
from app_order.models import Order
from .serializer import GetBillingSerializer, PostBillingSerializer


class OrderPayment(APIView):
    """Служба оплаты и проверки статуса опалты"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = GetBillingSerializer(data=request.query_params)
        order_id = request.query_params['order']
        if serializer.is_valid():
            order_status = Order.objects.filter(id=order_id).values('status_pay', 'payment_status')
            data = serializer.data
            data['paid'] = order_status[0]['status_pay']
            data['payment_status'] = order_status[0]['payment_status']
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = PostBillingSerializer(data=request.query_params)
        if serializer.is_valid():
            card = request.query_params['card_num']
            if int(card) % 2 == 0 and card[-1] != '0':
                serializer.save(payment_status=PayStatus.objects.get(id=2))
                return Response(request.query_params, status=status.HTTP_200_OK)
            elif int(card) % 2 == 0 and card[-1] == '0':
                code_err = random.randint(3, 5)
                serializer.save(payment_status=PayStatus.objects.get(id=code_err))
                return Response(request.query_params, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                serializer.save(payment_status=PayStatus.objects.get(id=3))
                return Response(request.query_params, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
