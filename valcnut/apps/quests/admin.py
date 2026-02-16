from django.contrib import admin
from .models import Quest, PlayerQuest

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'min_level', 'silver_reward', 'exp_reward')

@admin.register(PlayerQuest)
class PlayerQuestAdmin(admin.ModelAdmin):
    list_display = ('user', 'quest', 'status', 'progress', 'updated_at')
    list_filter = ('status', 'quest')
