from django.db import models
from django.conf import settings
from apps.items.models import InventoryItem

class Location(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    template = models.CharField(max_length=100)

    def __str__(self):
        return self.title

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

class Deal(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активна'),
        ('accepted', 'Завершена'),
        ('cancelled', 'Отменена'),
    )
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='initiated_deals')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_deals')

    initiator_silver = models.IntegerField(default=0)
    target_silver = models.IntegerField(default=0)

    initiator_accepted = models.BooleanField(default=False)
    target_accepted = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

class DealItem(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='items')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
