from django.contrib import admin
from .models import Skill, PlayerSkill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_level', 'mana_cost', 'base_damage', 'base_heal')

@admin.register(PlayerSkill)
class PlayerSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'level')
