from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('player', 'Игрок'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')

    # Game Stats
    level = models.IntegerField(default=0, verbose_name="Уровень")
    exp = models.IntegerField(default=0, verbose_name="Опыт")

    gold = models.IntegerField(default=0, verbose_name="Золото")
    silver = models.IntegerField(default=500, verbose_name="Серебро")
    diamonds = models.IntegerField(default=0, verbose_name="Алмазы")

    # Base Stats
    strength = models.IntegerField(default=3, verbose_name="Сила")
    agility = models.IntegerField(default=3, verbose_name="Ловкость")
    intuition = models.IntegerField(default=3, verbose_name="Интуиция")
    endurance = models.IntegerField(default=3, verbose_name="Выносливость")
    intelligence = models.IntegerField(default=3, verbose_name="Интеллект")
    wisdom = models.IntegerField(default=3, verbose_name="Мудрость")
    spirit = models.IntegerField(default=3, verbose_name="Дух")

    stat_points = models.IntegerField(default=0, verbose_name="Свободные очки")

    # Resources
    current_hp = models.FloatField(default=60, verbose_name="Текущее HP")
    current_mp = models.FloatField(default=50, verbose_name="Текущее MP")

    # State
    last_location = models.CharField(max_length=100, default='central_square', verbose_name="Локация")
    is_banned = models.BooleanField(default=False, verbose_name="Забанен")

    # Timestamps inherited from AbstractUser (date_joined)

    def __str__(self):
        return self.username

    @property
    def max_hp(self):
        return 30 + (self.endurance * 10)

    @property
    def max_mp(self):
        if self.level < 4:
            return 0
        return 20 + (self.intelligence * 10)

    def add_exp(self, amount):
        self.exp += amount
        # Simple level up logic: (level+1) * 100 exp for next level
        while self.exp >= (self.level + 1) * 100:
            self.exp -= (self.level + 1) * 100
            self.level += 1
            self.stat_points += 5
            # Full recovery on level up
            self.current_hp = self.max_hp
            self.current_mp = self.max_mp
        self.save()

    def get_battle_stats(self):
        stats = {
            'strength': self.strength,
            'agility': self.agility,
            'intuition': self.intuition,
            'endurance': self.endurance,
            'intelligence': self.intelligence,
            'wisdom': self.wisdom,
            'spirit': self.spirit,
            'min_dmg': 1,
            'max_dmg': 5,
            'armor': 0
        }
        # Add equipment bonuses
        for inv_item in self.inventory.filter(is_equipped=True):
            stats['strength'] += inv_item.get_bonus('bonus_strength')
            stats['agility'] += inv_item.get_bonus('bonus_agility')
            stats['intuition'] += inv_item.get_bonus('bonus_intuition')
            stats['endurance'] += inv_item.get_bonus('bonus_endurance')
            stats['armor'] += inv_item.get_bonus('bonus_armor')
            stats['min_dmg'] += inv_item.get_bonus('bonus_min_dmg')
            stats['max_dmg'] += inv_item.get_bonus('bonus_max_dmg')

        return stats

    def save(self, *args, **kwargs):
        # Initial HP/MP calculation if needed
        if self._state.adding:
            if self.level < 1: # If starting at level 0
                self.current_hp = 30 + (self.endurance * 10)
                self.current_mp = 0
            else:
                self.current_hp = self.max_hp
                self.current_mp = self.max_mp
        super().save(*args, **kwargs)
