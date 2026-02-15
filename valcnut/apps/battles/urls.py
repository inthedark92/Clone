from django.urls import path
from . import views

urlpatterns = [
    path('start_pve/', views.start_pve, name='start_pve'),
    path('start_duel/', views.start_duel, name='start_duel'),
]
