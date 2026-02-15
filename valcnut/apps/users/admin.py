from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'level', 'gold', 'silver', 'last_location', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Игровые параметры', {'fields': ('role', 'level', 'exp', 'gold', 'silver', 'stat_points')}),
        ('Характеристики', {'fields': ('strength', 'agility', 'intuition', 'endurance', 'intelligence', 'wisdom', 'spirit')}),
        ('Ресурсы', {'fields': ('current_hp', 'current_mp')}),
        ('Состояние', {'fields': ('last_location', 'is_banned')}),
    )

admin.site.register(User, CustomUserAdmin)
