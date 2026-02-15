from django.contrib import admin
from .models import Clan, BankAccount, MarketplaceItem

admin.site.register(Clan)
admin.site.register(BankAccount)
admin.site.register(MarketplaceItem)
