from rest_framework import serializers
from .models import Items, Order_item

class Itemserializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class Order_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_item
        fields = '__all__'