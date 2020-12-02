from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WarrantySerializer
from .models import Warranty
from rest_framework.parsers import JSONParser

# Create your views here.
@api_view(['POST'])
def req_warranty(request, itemUid):
    try:
        item = Warranty.objects.get(item_uid = itemUid)
    except Warranty.DoesNotExist:
        return Response({"message":"Warranty info not found"}, status = status.HTTP_404_NOT_FOUND)
  
    reqPars = JSONParser().parse(request)
    if not('reason' in reqPars) or not('availableCount' in reqPars):
        return Response({"message":"Bad request format"}, status = status.HTTP_400_BAD_REQUEST)

    warrData = WarrantySerializer(item).data
    warrData['comment'] = reqPars['reason']
    warrData = WarrantySerializer(item).data
    decision = dict(warrantyDate = warrData['warranty_date'])
    if warrData['status'] == 'ON_WARRANTY':
        warrData['status'] = 'USE_WARRANTY'
        warser = WarrantySerializer(item, data = warrData)
        if warser.is_valid():
            warser.save()
        if (reqPars['availableCount'] > 0):
            decision['decision'] = 'RETURN'
        else:
            decision['decision'] = 'FIXING'
    else:
        decision['decision'] = 'REFUSED'
    return Response(decision, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def get_post_del(request, itemUid):
    if request.method == 'GET':
        try:
            item = Warranty.objects.get(item_uid = itemUid)
        except Warranty.DoesNotExist:
            return Response({"message":"Warranty info not found"}, status = status.HTTP_404_NOT_FOUND)

        ser = WarrantySerializer(item).data
        req = dict(itemUid = ser['item_uid'], warrantyDate = ser['warranty_date'], status = ser['status'])
        return Response(req, status = status.HTTP_200_OK)

    elif request.method == 'POST':
        warr = dict(status = 'ON_WARRANTY', item_uid = itemUid, comment = 'NoComment')
        warSer = WarrantySerializer(data = warr)
        if warSer.is_valid():
            warSer.save()
            return Response({"message":"Warranty started for item"}, status = status.HTTP_204_NO_CONTENT)

    elif request.method == 'DELETE':
        try:
            item = Warranty.objects.get(item_uid = itemUid)
        except Warranty.DoesNotExist:
            return Response({"message":"Warranty info not found"}, status = status.HTTP_404_NOT_FOUND)
      
        ser = WarrantySerializer(item).data
        ser['status'] = 'REMOVED_FROM_WARRANTY'
        seritem = WarrantySerializer(item, data = ser)
        if seritem.is_valid():
            seritem.save()
        return Response({"message":"Warranty closed for item"}, status = status.HTTP_204_NO_CONTENT)