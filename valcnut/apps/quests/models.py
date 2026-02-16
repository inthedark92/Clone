from django.db import models
from django.conf import settings

class Quest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    min_level = models.IntegerField(default=1)
    silver_reward = models.IntegerField(default=0)
    exp_reward = models.IntegerField(default=0)
    item_reward = models.ForeignKey('items.Item', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class PlayerQuest(models.Model):
    STATUS_CHOICES = (
        ('available', 'Доступен'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quests')
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    progress = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.quest.title}"
