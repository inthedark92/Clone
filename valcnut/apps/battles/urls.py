from django.urls import path
from . import views

urlpatterns = [
    path('start_pve/', views.start_pve, name='start_pve'),
]
