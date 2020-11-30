from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrdersSerializer
from .models import Orders
from rest_framework.parsers import JSONParser
import requests

# Create your views here.
# @api_view(['GET', 'POST'])
# def get_post_orders(request, userUid):
#     if request.method == 'GET':
#         orders = Orders.objects.all().filter(user_uid = userUid)
#         serializer_orders = OrdersSerializer(orders, many = True).data
#         for item in serializer_orders:
#             item['orderUid']=item['order_uid']
#             item['orderDate'] = item['order_date']
#             item['itemUid'] = item['item_uid']
#             del item['order_uid'], item['order_date'], item['item_uid'], item['id'], item['user_uid']
#         return Response (serializer_orders, status=status.HTTP_200_OK)

#     elif request.method == 'POST':
#         parsReq = JSONParser().parse(requests)
#         if (not('model' in parsReq)) or (not('size' in parsReq)):
#             return Response({'message':'Bad request format'}, status = status.HTTP_400_BAD_REQUEST)
#         order = dict (status = 'PAID', user_uid = userUid)
#         serord = OrdersSerializer(data = order)
#         if serord.is_valid():
#             serord.save()
#         parsReq.update({'orderUid': serord.data['order_uid']})
#         warehousReq = requests.post('https://lab2-warehouse-litvinov.herokuapp.com/api/v1/warehouse', json= parsReq)
#         if warehousReq.status_code == 409:
#             return Response({'message':'Item not available'}, status=status.HTTP_409_CONFLICT)
#         serord.data['item_uid'] = warehousReq.json
        



# @api_view(['GET'])
# def get_order(request, userUid, orderUid):
#     try:
#         order = Orders.objects.get(user_uid = userUid, order_uid = orderUid)
#     except:
#         return Response({'message':'Order not found'}, status = status.HTTP_404_NOT_FOUND)
#     ser = OrdersSerializer(order).data
#     req = dict(orderUid = ser['order_uid'], orderDate = ser['order_date'], itemUid = ser['item_uid'], status = ser['status'])
#     return Response (req, status=status.HTTP_200_OK)

#@api_view(['POST'])

#@api_view(['DELETE'])