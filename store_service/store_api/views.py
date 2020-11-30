from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StoreSerializer
from .models import Store
from rest_framework.parsers import JSONParser
import requests
import json

# Create your views here.
#@api_view(['GET'])
#def get_orders(request, user_uid):    

#@api_view(['GET'])
#def get_order(request, user_uid, order_uid):

# @api_view(['POST'])
# def req_warranty(request, userUid, orderUid):
#     user = Store.objects.get(user_uid = userUid)
#     if Store.DoesNotExist():
#         return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     parsReq = JSONParser().parse(requests)
#     if (not('reason' in parsReq)
#         return Response({"message":"Bad request format"}, status=status.HTTP_400_BAD_REQUEST)
    
#     warranty = requests.post('https://lab2-orders-litvinov.herokuapp.com/api/v1/orders/{}/warranty'.format(orderUid), json=parsReq)
#     if warranty.status_code == 404:
#         return Response({"message":"Order not found"}, status=status.HTTP_409_CONFLICT)
    
#     warranty = warranty.json()
#     warranty.update({'orderUid':orderUid})
#     return Response(warranty, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def do_purchase(request, userUid):
#     user = Store.objects.get(user_uid = userUid)
#     if Store.DoesNotExist():
#         return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)

#     parsReq = JSONParser().parse(requests)
#     if (not('model' in parsReq)) or (not('size' in parsReq))
#         return Response({"message":"Bad request format"}, status=status.HTTP_400_BAD_REQUEST)
    
#     order = requests.post('https://lab2-orders-litvinov.herokuapp.com/api/v1/orders/{}'.format(userUid), json=parsReq)
#     if order.status_code == 409:
#         return Response({"message":"Item not available"}, status=status.HTTP_409_CONFLICT)

#     order = orde.json()
#     return Response({"message":"Item purchased"}, status = status.HTTP_201_CREATED, headers = {
#             "Location":f'http//https://lab2-orders-litvinov.herokuapp.com/api/v1/orders/{user_uid}/purchase/{order_uid}'.format(user_uid = user_uid, order_uid = order["orderUid"])})

# @api_view(['DELETE'])
# def req_refund(request, user_uid, orderUid):
    user = Store.objects.get(user_uid = userUid)
    if Store.DoesNotExist():
        return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    orderDel = requests.delete('https://lab2-orders-litvinov.herokuapp.com/api/v1/orders/{}'.format(orderUid))
    if orderDel.status_code == 404:
        return Response({"message":"Order not found"}, status=status.HTTP_409_CONFLICT)
    
    return Response({"message":"Item returned"},status=status.HTTP_204_NO_CONTENT)