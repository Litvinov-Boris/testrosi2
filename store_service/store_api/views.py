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
@api_view(['GET'])
def get_orders(request, userUid):
    try:
        user = Store.objects.get(user_uid = userUid)
    except Store.DoesNotExist:
        return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    ordersReq = requests.get('https://lab2-orders-livinov.herokuapp.com/api/v1/orders/{}'.format(userUid))
    if ordersReq.status_code == 404:
        return Response({"message":"Order not found"}, status=status.HTTP_409_CONFLICT)
    ordersReq = ordersReq.json()

    for item in ordersReq:
        warehouseReq = requests.get('https://lab2-warehouse-litvinov.herokuapp.com/api/v1/warehouse/{}'.format(item['itemUid']))
        if warehouseReq.status_code == 404:
            return Response({"message":"OrderItem not found"}, status=status.HTTP_409_CONFLICT)
        warehouseReq = warehouseReq.json()

        warrantyReq = requests.get('https://lab2-warranty-litvinov.herokuapp.com/api/v1/warranty/{}'.format(item['itemUid']))
        if warrantyReq.status_code == 404:
            return Response({"message":"Warranty not found"}, status=status.HTTP_409_CONFLICT)
        warrantyReq = warrantyReq.json()

        item['date'] = item['orderDate']
        item['model'] = warehouseReq['model']
        item['size'] = warehouseReq['size']
        item['warrantyDate'] = warrantyReq['warrantyDate']
        item['warrantyStatus'] = warrantyReq['status']
        del item['itemUid'], item['status'], item['orderDate']
    return Response(ordersReq, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_order(request, userUid, orderUid):
    try:
        user = Store.objects.get(user_uid = userUid)
    except Store.DoesNotExist:
        return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    orderReq = requests.get('https://lab2-orders-livinov.herokuapp.com/api/v1/orders/{userUid}/{orderUid}'.format(userUid = userUid, orderUid = orderUid))
    if orderReq.status_code == 404:
        return Response({"message":"Order not found"}, status=status.HTTP_409_CONFLICT)
    orderReq = orderReq.json()

    warehouseReq = requests.get('https://lab2-warehouse-litvinov.herokuapp.com/api/v1/warehouse/{}'.format(orderReq['itemUid']))
    if warehouseReq.status_code == 404:
        return Response({"message":"OrderItem not found"}, status=status.HTTP_409_CONFLICT)
    warehouseReq = warehouseReq.json()

    warrantyReq = requests.get('https://lab2-warranty-litvinov.herokuapp.com/api/v1/warranty/{}'.format(orderReq['itemUid']))
    if warrantyReq.status_code == 404:
        return Response({"message":"Warranty not found"}, status=status.HTTP_409_CONFLICT)
    warrantyReq = warrantyReq.json()

    res = dict(orderUid = orderUid, date = orderReq['orderDate'], model = warehouseReq['model'], size = warehouseReq['size'], warrantyDate = warrantyReq['warrantyDate'], warrantyStatus = warrantyReq['status'])
    return Response(res, status=status.HTTP_200_OK)

@api_view(['POST', 'DELETE'])
def req_warranty(request, userUid, orderUid):
    try:
        user = Store.objects.get(user_uid = userUid)
    except Store.DoesNotExist():
        return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
   
    if request.method == 'POST':
        parsReq = JSONParser().parse(request)
        if (not('reason' in parsReq)):
            return Response({"message":"Bad request format"}, status=status.HTTP_400_BAD_REQUEST)
    
        warranty = requests.post('https://lab2-orders-livinov.herokuapp.com/api/v1/orders/{}/warranty'.format(orderUid), json=parsReq)
        if warranty.status_code == 404:
            return Response({"message":"Order not found"}, status=status.HTTP_409_CONFLICT)
    
        warranty = warranty.json()
        warranty.update({'orderUid':orderUid})
        return Response(warranty, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        orderDel = requests.delete('https://lab2-orders-livinov.herokuapp.com/api/v1/orders/{}'.format(orderUid))
        if orderDel.status_code == 404:
            return Response({"message":"Order not found"}, status=status.HTTP_409_CONFLICT)
    
        return Response({"message":"Item returned"},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def do_purchase(request, userUid):
    try:
        user = Store.objects.get(user_uid = userUid)
    except Store.DoesNotExist():
        return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)

    parsReq = JSONParser().parse(request)
    if (not('model' in parsReq)) or (not('size' in parsReq)):
        return Response({"message":"Bad request format"}, status=status.HTTP_400_BAD_REQUEST)
    
    order = requests.post('https://lab2-orders-livinov.herokuapp.com/api/v1/orders/{}'.format(userUid), json=parsReq)
    if order.status_code == 409:
        return Response({"message":"Item not available"}, status=status.HTTP_409_CONFLICT)

    order = order.json()
    return Response({"message":"Item purchased"}, status = status.HTTP_201_CREATED, headers = {
            "Location":f'http//https://lab2-orders-livinov.herokuapp.com/api/v1/orders/{userUid}/purchase/{order["orderUid"]}'})
    