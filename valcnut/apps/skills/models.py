from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    min_level = models.IntegerField(default=1)
    mana_cost = models.IntegerField(default=0)
    base_damage = models.IntegerField(default=0)
    base_heal = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class PlayerSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} (Lvl {self.level})"
