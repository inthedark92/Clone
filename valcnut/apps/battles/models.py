from django.db import models
from apps.characters.models import Character

class Battle(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    )
    TYPE_CHOICES = (
        ('pvp', 'PvP'),
        ('pve', 'PvE'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    battle_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    current_turn = models.IntegerField(default=1)
    log = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

class BattleParticipant(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name='participants')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True)
    npc_id = models.CharField(max_length=100, null=True, blank=True)
    team = models.IntegerField()
    hp_snapshot = models.IntegerField()
    stats_snapshot = models.JSONField()
    is_winner = models.BooleanField(default=False)
