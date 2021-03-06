from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Itemserializer, Order_itemSerializer
from .models import Items, Order_item
from rest_framework.parsers import JSONParser
import requests
# Create your views here.

@api_view(['GET', 'DELETE'])
def get_del_ware(request, orderItemUid):
    try:
        orderItem = Order_item.objects.get(order_item_uid = orderItemUid)
        item = Items.objects.get(id = orderItem.item_id)
        itemData = Itemserializer(item).data
    except Order_item.DoesNotExist:
        return Response({'message':'OrderItem not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        req = dict(model = itemData['model'], size = itemData['size'])
        return Response(req, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        orderItemData = Order_itemSerializer(orderItem).data
        if orderItemData['canceled']==True:
            return Response({'message':'Item returned'}, status=status.HTTP_204_NO_CONTENT)
        itemData['available_count']+=1
        item = Itemserializer(item, data = itemData)
        if item.is_valid():
            item.save()
        orderItemData['canceled']=True
        orderItem = Order_itemSerializer(orderItem, data = orderItemData)
        if orderItem.is_valid():
            orderItem.save()
        return Response({'message':'Item returned'}, status=status.HTTP_204_NO_CONTENT)
        

@api_view(['POST'])
def take_item(request):
    parseReq = JSONParser().parse(request)
    if (not ('model' in parseReq)) or (not('size' in parseReq) or (not('orderUid' in parseReq))):
        return Response({'message':'Bad request format'}, status=status.HTTP_400_BAD_REQUEST )

    try:
        item = Items.objects.get(model = parseReq['model'], size = parseReq['size'])
    except:
        return Response({'message':'Requested item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    itemData = Itemserializer(item).data
    if itemData['available_count'] == 0:
        return Response({'message':'Item not available'}, status=status.HTTP_409_CONFLICT)
    
    order = dict(order_uid = parseReq['orderUid'], item_id = itemData['id'])
    if "orderItemUid" in parseReq:
        order['order_item_uid'] = parseReq['orderItemUid']
    orderItem = Order_itemSerializer(data = order)
    if orderItem.is_valid():
        orderItem.save()

    itemData['available_count']-=1
    item = Itemserializer(item, data = itemData)
    if item.is_valid():
        item.save()

    ser = orderItem.data
    req = dict(orderItemUid = ser['order_item_uid'], orderUid = ser['order_uid'], model = parseReq['model'], size = parseReq['size'])
    return Response(req, status=status.HTTP_200_OK)
        
    
@api_view(['POST'])
def req_warr(request, orderItemUid):
    try:
        order = Order_item.objects.get(order_item_uid = orderItemUid)
    except Order_item.DoesNotExist:
        return Response({'message':'Requested item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    parsReq = JSONParser().parse(request)
    if not('reason' in parsReq):
        return Response({"message":"Bad request format"}, status=status.HTTP_400_BAD_REQUEST)
 
    orderdata = Order_itemSerializer(order).data
    item = Items.objects.get(id = orderdata['item_id'])
    itemdata = Itemserializer(item).data
    reqwarranty = dict(availableCount = itemdata['available_count'],reason = parsReq['reason'])
    requestWar = requests.post('https://lab2-warranty-litvinov.herokuapp.com/api/v1/warranty/{}/warranty'.format(orderItemUid), json=reqwarranty)
    if requestWar.status_code == 404:
        return Response({'message':'Warranty not found for itemUid \'{}\''.format(orderItemUid)}, status=status.HTTP_404_NOT_FOUND)
    return Response(requestWar.json(),status=status.HTTP_200_OK)
