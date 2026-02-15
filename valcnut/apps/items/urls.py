from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory_view, name='inventory'),
    path('repair/<int:item_id>/', views.repair_item, name='repair_item'),
    path('enhance/<int:item_id>/', views.enhance_item, name='enhance_item'),
    path('market/', views.market_view, name='market'),
    path('market/buy/<int:item_id>/', views.buy_item, name='buy_item'),
    path('commission/', views.commission_shop_view, name='commission_shop'),
    path('commission/list/<int:inv_item_id>/', views.list_on_commission, name='list_commission'),
    path('commission/buy/<int:comm_item_id>/', views.buy_commission_item, name='buy_commission_item'),
]
