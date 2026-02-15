from django.db import models
from django.conf import settings

class Character(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)

    # Base Stats
    strength = models.IntegerField(default=3)
    agility = models.IntegerField(default=3)
    intuition = models.IntegerField(default=3)
    endurance = models.IntegerField(default=3)
    intelligence = models.IntegerField(default=3)
    wisdom = models.IntegerField(default=3)
    spirit = models.IntegerField(default=3)

    stat_points = models.IntegerField(default=0)

    current_hp = models.FloatField(default=60)
    current_mp = models.FloatField(default=50)

    location_id = models.CharField(max_length=100, default='central_square')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def max_hp(self):
        return 30 + (self.endurance * 10)

    @property
    def max_mp(self):
        return 20 + (self.wisdom * 10)
