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
    intelligence = models.IntegerField(default=0, verbose_name="Интеллект")
    wisdom = models.IntegerField(default=0, verbose_name="Мудрость")
    spirit = models.IntegerField(default=0, verbose_name="Дух")

    stat_points = models.IntegerField(default=5, verbose_name="Свободные очки")

    # Statistics
    sub_levels_completed = models.IntegerField(default=0, verbose_name="Завершено подуровней")
    total_xp = models.IntegerField(default=0, verbose_name="Всего опыта")

    monster_wins = models.IntegerField(default=0, verbose_name="Побед (мобы)")
    monster_draws = models.IntegerField(default=0, verbose_name="Ничьих (мобы)")
    monster_losses = models.IntegerField(default=0, verbose_name="Поражений (мобы)")

    player_wins = models.IntegerField(default=0, verbose_name="Побед (игроки)")
    player_draws = models.IntegerField(default=0, verbose_name="Ничьих (игроки)")
    player_losses = models.IntegerField(default=0, verbose_name="Поражений (игроки)")

    # Clan & Alliance
    clan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Клан")
    alliance = models.CharField(max_length=100, blank=True, null=True, verbose_name="Альянс")

    # Resources
    current_hp = models.FloatField(default=60, verbose_name="Текущее HP")
    current_mp = models.FloatField(default=0, verbose_name="Текущее MP")

    # State
    last_location = models.CharField(max_length=100, default='novice_hall', verbose_name="Локация")
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
        self.total_xp += amount

        # Level up logic: each level has 5 sub-levels for example, or just use the requirements
        # Percent progress to next sub-level etc.
        # Let's say level up is at 1000 exp, and every 200 exp is a sub-level.
        # The prompt says: "Sub-levels completed", "Percent progress to next sub-level"

        # Simple placeholder for sub-level logic:
        # 1 level = 1000 exp, 10 sub-levels (100 exp each)
        sub_level_cap = 100
        level_cap = 1000

        while self.exp >= level_cap:
            self.exp -= level_cap
            self.level += 1
            self.stat_points += 5
            self.sub_levels_completed = 0
            self.current_hp = self.max_hp
            self.current_mp = self.max_mp

        self.sub_levels_completed = self.exp // sub_level_cap
        self.save()

    @property
    def sub_level_progress_percent(self):
        sub_level_cap = 100
        progress = self.exp % sub_level_cap
        return int((progress / sub_level_cap) * 100)

    @property
    def next_level_exp(self):
        return 1000

    @property
    def evasion(self):
        # 1 agility = 5 evasion points
        return self.agility * 5

    @property
    def critical_chance(self):
        # 1 intuition = 5 critical points
        return self.intuition * 5

    @property
    def defense(self):
        # 1 endurance = 2 defense points + armor from equipment
        stats = self.get_battle_stats()
        return (self.endurance * 2) + stats['armor']

    @property
    def damage_range(self):
        stats = self.get_battle_stats()
        # Strength adds to damage
        bonus = self.strength // 2
        return f"{stats['min_dmg'] + bonus}-{stats['max_dmg'] + bonus}"

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
