from django.contrib import admin
from .models import Item, InventoryItem

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'req_level', 'price_gold', 'price_silver')
    list_filter = ('item_type',)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'is_equipped', 'slot')
    list_filter = ('is_equipped', 'slot')
