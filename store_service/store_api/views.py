from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StoreSerializer
from .models import Store

# Create your views here.
@api_view(['GET'])
def get_orders(request, user_uid):
    try:
        user = Store.objects.get(user_uid = user_uid)
    except Store.DoesNotExist
        return Response({'message' : 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    

@api_view(['GET'])
def get_order(request, user_uid, order_uid):

@api_view(['POST'])
def req_warranty(request, user_uid, order_uid):

@api_view(['POST'])
def do_purchase(request, user_uid):

@api_view(['POST'])
def req_refund(request, user_uid, order_uid):