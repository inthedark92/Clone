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
    level = models.IntegerField(default=1, verbose_name="Уровень")
    exp = models.IntegerField(default=0, verbose_name="Опыт")

    gold = models.IntegerField(default=0, verbose_name="Золото")
    silver = models.IntegerField(default=500, verbose_name="Серебро")

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
        return 20 + (self.wisdom * 10)

    def save(self, *args, **kwargs):
        # Initial HP/MP calculation if needed
        if self._state.adding:
            self.current_hp = self.max_hp
            self.current_mp = self.max_mp
        super().save(*args, **kwargs)
