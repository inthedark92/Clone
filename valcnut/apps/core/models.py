from django.db import models
from django.conf import settings
from apps.items.models import InventoryItem

class Clan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='led_clans')
    created_at = models.DateTimeField(auto_now_add=True)

class BankAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance_gold = models.IntegerField(default=0)
    balance_silver = models.IntegerField(default=0)

class MarketplaceItem(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price_gold = models.IntegerField(default=0)
    price_silver = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    CHANNEL_CHOICES = (
        ('world', 'Мировой'),
        ('location', 'Локация'),
        ('trade', 'Торговый'),
        ('group', 'Группа'),
        ('clan', 'Клан'),
        ('alliance', 'Альянс'),
        ('private', 'Личный'),
        ('system', 'Системный'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    text = models.TextField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='world')
    location = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.channel}] {self.user.username}: {self.text[:50]}"
