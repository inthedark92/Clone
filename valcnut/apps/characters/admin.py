from django.contrib import admin
from .models import Character

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'level', 'current_hp')
    search_fields = ('name', 'user__username')
