from django.db import models
from apps.characters.models import Character

class Item(models.Model):
    TYPE_CHOICES = (
        ('weapon', 'Weapon'),
        ('armor', 'Armor'),
        ('helmet', 'Helmet'),
        ('gloves', 'Gloves'),
        ('boots', 'Boots'),
        ('shield', 'Shield'),
        ('ring', 'Ring'),
        ('amulet', 'Amulet'),
        ('potion', 'Potion'),
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

    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_equipped = models.BooleanField(default=False)
    slot = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.character.name} - {self.item.name}"
