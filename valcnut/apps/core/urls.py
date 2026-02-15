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
    path('<slug:slug>/', views.location_view, name='location'),
]
