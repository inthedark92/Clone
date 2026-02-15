from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory_view, name='inventory'),
    path('repair/<int:item_id>/', views.repair_item, name='repair_item'),
    path('enhance/<int:item_id>/', views.enhance_item, name='enhance_item'),
]
