from django.urls import path
from . import views

urlpatterns = [
    path('character/', views.character_view, name='character'),
    path('character/increase_stat/', views.increase_stat, name='increase_stat'),
]
