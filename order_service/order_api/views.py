from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrdersSerializer
from .models import Orders

# Create your views here.
@api_view(['GET', 'POST'])
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

@api_view(['GET'])
def get_order(request, userUid, orderUid):
    try:
        order = Orders.objects.get(user_uid = userUid, order_uid = orderUid)
    except:
        return Response({'message':'Order not found'}, status = status.HTTP_404_NOT_FOUND)
    ser = OrdersSerializer(order).data
    req = dict(orderUid = ser['order_uid'], orderDate = ser['order_date'], itemUid = ser['item_uid'], status = ser['status'])
    return Response (req, status=status.HTTP_200_OK)
