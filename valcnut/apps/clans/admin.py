from django.contrib import admin
from .models import Clan, ClanMember

@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag', 'leader', 'level', 'created_at')
    search_fields = ('name', 'tag')

@admin.register(ClanMember)
class ClanMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'clan', 'rank', 'joined_at')
    list_filter = ('clan', 'rank')
