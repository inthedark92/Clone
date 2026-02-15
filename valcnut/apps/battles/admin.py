from django.contrib import admin
from .models import Battle, BattleParticipant

class BattleParticipantInline(admin.TabularInline):
    model = BattleParticipant
    extra = 0

@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'battle_type', 'current_turn', 'created_at')
    inlines = [BattleParticipantInline]

@admin.register(BattleParticipant)
class BattleParticipantAdmin(admin.ModelAdmin):
    list_display = ('battle', 'user', 'team', 'hp_snapshot', 'is_winner')
