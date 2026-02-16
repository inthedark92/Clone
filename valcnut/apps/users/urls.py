from django.urls import path
from . import views

urlpatterns = [
    path('character/', views.character_view, name='character'),
    path('character/<int:user_id>/', views.character_info_view, name='character_info_id'),
    path('character/<str:username>/', views.character_info_view, name='character_info'),
    path('increase_stat/', views.increase_stat, name='increase_stat'),
]
