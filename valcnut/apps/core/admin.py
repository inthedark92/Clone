from django.contrib import admin
from .models import Clan, BankAccount, MarketplaceItem, ChatMessage, Deal, DealItem, Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'template')
    search_fields = ('title', 'slug')

admin.site.register(Clan)
admin.site.register(BankAccount)
admin.site.register(MarketplaceItem)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipient', 'channel', 'text', 'created_at')
    list_filter = ('channel',)

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'target', 'status', 'created_at')
    list_filter = ('status',)

admin.site.register(DealItem)
