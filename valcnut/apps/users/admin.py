from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'level', 'gold', 'silver', 'diamonds', 'last_location', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Игровые параметры', {'fields': ('role', 'level', 'exp', 'gold', 'silver', 'diamonds', 'stat_points', 'clan', 'alliance', 'group_id')}),
        ('Характеристики', {'fields': ('strength', 'agility', 'intuition', 'endurance', 'intelligence', 'wisdom', 'spirit')}),
        ('Ресурсы', {'fields': ('current_hp', 'current_mp')}),
        ('Статистика', {'fields': ('monster_wins', 'monster_draws', 'monster_losses', 'player_wins', 'player_draws', 'player_losses', 'total_xp', 'sub_levels_completed')}),
        ('Состояние', {'fields': ('last_location', 'is_banned')}),
    )

admin.site.register(User, CustomUserAdmin)
