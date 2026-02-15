from django.db import models
from django.conf import settings

class Item(models.Model):
    TYPE_CHOICES = (
        ('weapon', 'Оружие'),
        ('armor', 'Броня'),
        ('helmet', 'Шлем'),
        ('gloves', 'Перчатки'),
        ('boots', 'Сапоги'),
        ('shield', 'Щит'),
        ('ring', 'Кольцо'),
        ('amulet', 'Амулет'),
        ('potion', 'Зелье'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    item_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    req_level = models.IntegerField(default=1)
    req_strength = models.IntegerField(default=0)
    req_agility = models.IntegerField(default=0)
    req_intuition = models.IntegerField(default=0)

    bonus_strength = models.IntegerField(default=0)
    bonus_agility = models.IntegerField(default=0)
    bonus_intuition = models.IntegerField(default=0)
    bonus_endurance = models.IntegerField(default=0)
    bonus_armor = models.IntegerField(default=0)
    bonus_min_dmg = models.IntegerField(default=0)
    bonus_max_dmg = models.IntegerField(default=0)

    price_gold = models.IntegerField(default=0)
    price_silver = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_equipped = models.BooleanField(default=False)
    slot = models.CharField(max_length=50, null=True, blank=True)

    durability_current = models.IntegerField(default=100)
    durability_max = models.IntegerField(default=100)
    enhancement_level = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.item.name} (+{self.enhancement_level})"

    @property
    def is_active(self):
        return self.durability_current > 0

    def get_bonus(self, attr):
        if not self.is_active:
            return 0
        base_val = getattr(self.item, attr, 0)
        if base_val > 0:
            # Each enhancement level adds +1 to the stat
            return base_val + self.enhancement_level
        return base_val
