from django.urls import path
from . import views

urlpatterns = [
    path('', views.location_view, name='game_index'),
    path('extract/', views.extract_resource, name='extract_resource'),
    path('bank/', views.bank_view, name='bank'),
    path('bank/deposit/', views.bank_deposit, name='bank_deposit'),
    path('bank/withdraw/', views.bank_withdraw, name='bank_withdraw'),
    path('tavern/', views.tavern_view, name='tavern'),
    path('tavern/buy/<int:item_id>/', views.tavern_buy, name='tavern_buy'),
    path('deals/', views.deals_view, name='deals'),
    path('deals/initiate/<int:user_id>/', views.initiate_deal, name='initiate_deal'),
    path('deals/view/<int:deal_id>/', views.view_deal, name='view_deal'),
    path('deals/update_silver/<int:deal_id>/', views.deal_update_silver, name='deal_update_silver'),
    path('deals/add_item/<int:deal_id>/<int:item_id>/', views.deal_add_item, name='deal_add_item'),
    path('deals/remove_item/<int:deal_id>/<int:deal_item_id>/', views.deal_remove_item, name='deal_remove_item'),
    path('deals/accept/<int:deal_id>/', views.deal_accept, name='deal_accept'),
    path('deals/cancel/<int:deal_id>/', views.deal_cancel, name='deal_cancel'),
    path('map/', views.map_view, name='map'),
    path('mod_panel/', views.mod_panel_view, name='mod_panel'),
    path('<slug:slug>/', views.location_view, name='location'),
]
