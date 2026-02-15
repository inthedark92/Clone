from django.db import models
from apps.characters.models import Character
from apps.items.models import InventoryItem

class Clan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    leader = models.ForeignKey(Character, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class BankAccount(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

class MarketplaceItem(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    seller = models.ForeignKey(Character, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
