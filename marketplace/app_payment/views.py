from django.shortcuts import redirect
from django.views import View
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializer import PostOrderSerializer
from .tasks import handle_payment


class AddOrder(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PostOrderSerializer(data=request.query_params)
        if serializer.is_valid():
            serializer.save()
            return Response(request.query_params, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Test(View):
    def get(self, request):
        handle_payment.delay(1, 123, 100)
        return redirect('/cart/')
