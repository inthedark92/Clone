from rest_framework import serializers
from .models import Item, InventoryItem, CommissionItem

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    class Meta:
        model = InventoryItem
        fields = '__all__'

class CommissionItemSerializer(serializers.ModelSerializer):
    inventory_item = InventoryItemSerializer(read_only=True)
    class Meta:
        model = CommissionItem
        fields = '__all__'
