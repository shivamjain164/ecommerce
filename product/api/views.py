from . import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics,mixins
from product import models

class Allorders(APIView):
    def get(self,request):
        orders = models.OrderPlaced.objects.all()
        serializer = serializers.AllordersSerializer(orders, many=True)
        # print (serializer.data)
        return Response(serializer.data)
    
class OrderByUser(APIView):
    def get(self,request,username):
        orders = models.OrderPlaced.objects.filter(user__username=username)
        serializer = serializers.AllordersSerializer(orders, many=True)
        return Response(serializer.data)