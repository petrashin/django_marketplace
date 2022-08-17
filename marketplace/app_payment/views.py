from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializer import PostOrderSerializer
from .tasks import handle_payment


class AddOrder(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PostOrderSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['order_id'].status_pay is False:
                handle_payment.delay(request.data)
                return Response(request.data, status=status.HTTP_200_OK)
            else:
                return Response("Заказ уже оплачен", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
