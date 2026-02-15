from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from apps.users.views import RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),

    # Auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # Game
    path('game/', include('apps.core.urls')),
    path('game/items/', include('apps.items.urls')),
]
