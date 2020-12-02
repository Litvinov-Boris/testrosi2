from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrdersSerializer
from .models import Orders
from rest_framework.parsers import JSONParser
import requests
import json

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def get_post_orders(request, userUid):
    if request.method == 'GET':
        orders = Orders.objects.all().filter(user_uid = userUid)
        serializer_orders = OrdersSerializer(orders, many = True).data
        for item in serializer_orders:
            item['orderUid']=item['order_uid']
            item['orderDate'] = item['order_date']
            item['itemUid'] = item['item_uid']
            del item['order_uid'], item['order_date'], item['item_uid'], item['id'], item['user_uid']
        return Response (serializer_orders, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        parsReq = JSONParser().parse(request)
        if (not('model' in parsReq)) or (not('size' in parsReq)):
            return Response({'message':'Bad request format'}, status = status.HTTP_400_BAD_REQUEST)

        order = dict (status = 'BUILD', user_uid = userUid)
        serord = OrdersSerializer(data = order)
        if serord.is_valid():
            serord.save()
        parsReq.update({'orderUid': serord.data['order_uid']})
        warehousReq = requests.post('https://lab2-warehouse-litvinov.herokuapp.com/api/v1/warehouse', json= parsReq)
        if warehousReq.status_code == 404 or warehousReq.status_code == 409:
            return Response({'message':'Item not available'}, status=status.HTTP_409_CONFLICT)
        warehousReq = warehousReq.json()

        orderN = Orders.objects.get(order_uid = serord.data['order_uid'])
        orderData = OrdersSerializer(orderN).data
        orderData['status'] = 'PAID'
        orderData['item_uid'] = warehousReq['orderItemUid']
        orderN = OrdersSerializer(orderN, data = orderData)
        if orderN.is_valid():
            orderN.save()

        warrantyReq = requests.post('https://lab2-warranty-litvinov.herokuapp.com/api/v1/warranty/{}'.format(warehousReq['orderItemUid']))
        return Response({"orderUid": serord.data["order_uid"]}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        try:
            order = Orders.objects.get(order_uid = userUid)
        except Orders.DoesNotExist:
            return Response({"message":"Order not found"}, status=status.HTTP_404_NOT_FOUND)
    
        orderData = OrdersSerializer(order).data
        delreqwareh = requests.delete('https://lab2-warehouse-litvinov.herokuapp.com/api/v1/warehouse/{}'.format(orderData['item_uid']))
        delreqwarra = requests.delete('https://lab2-warranty-litvinov.herokuapp.com/api/v1/warranty/{}'.format(orderData['item_uid']))
        # orderData['status'] = 'REFUNDED'
        # order = OrdersSerializer(order, data= orderData)
        # if order.is_valid():
        #     order.save()
        order.delete()
        return Response({"message":"Order returned"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_order(request, userUid, orderUid):
    try:
        order = Orders.objects.get(user_uid = userUid, order_uid = orderUid)
    except:
        return Response({'message':'Order not found'}, status = status.HTTP_404_NOT_FOUND)
    ser = OrdersSerializer(order).data
    req = dict(orderUid = ser['order_uid'], orderDate = ser['order_date'], itemUid = ser['item_uid'], status = ser['status'])
    return Response (req, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_warranty(request, orderUid):
    try:
        order = Orders.objects.get(order_uid = orderUid)
    except Orders.DoesNotExist():
        return Response({"message":"Order not found"}, status=status.HTTP_404_NOT_FOUND)
    
    parsReq = JSONParser().parse(request)
    if not('reason' in parsReq):
        return Response({"message":"Bad request format"}, status=status.HTTP_400_BAD_REQUEST)
    
    orderData = OrdersSerializer(order).data
    warehousereq = requests.post('https://lab2-warehouse-litvinov.herokuapp.com/api/v1/warehouse/{}/warranty'.format(orderData['item_uid']), json = parsReq)
    if warehousereq.status_code == 404 or warehousereq.status_code == 409:
        return Response({"message":"Order not found"}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(warehousereq.json(), status=status.HTTP_200_OK)   

