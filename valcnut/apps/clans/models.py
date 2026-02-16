from django.db import models
from django.conf import settings

class Clan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tag = models.CharField(max_length=10, unique=True)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='led_clan')
    description = models.TextField(blank=True)
    silver_bank = models.IntegerField(default=0)
    gold_bank = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=1)

    def __str__(self):
        return f"[{self.tag}] {self.name}"

class ClanMember(models.Model):
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name='members')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clan_membership')
    rank = models.CharField(max_length=50, default='Private')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.clan.name}"
