from django.urls import path
from . import views

urlpatterns = [
    path('start_pve/', views.start_pve, name='start_pve'),
    path('combat/<int:battle_id>/', views.combat_view, name='combat'),
    path('combat/<int:battle_id>/turn/', views.combat_turn, name='combat_turn'),
    path('start_duel/', views.start_duel, name='start_duel'),
]
