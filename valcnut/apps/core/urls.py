from django.urls import path
from . import views

urlpatterns = [
    path('', views.location_view, name='game_index'),
    path('<slug:slug>/', views.location_view, name='location'),
]
