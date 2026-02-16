from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from apps.users.views import RegisterView, character_info_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),

    # Auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('character/<int:user_id>/', character_info_view, name='character_info_direct'),

    # Game
    path('game/', include('apps.core.urls')),
    path('game/items/', include('apps.items.urls')),
    path('game/users/', include('apps.users.urls')),
    path('game/battles/', include('apps.battles.urls')),
    path('game/quests/', include('apps.quests.urls')),
    path('game/mail/', include('apps.mail.urls')),
    path('game/clans/', include('apps.clans.urls')),
    path('game/skills/', include('apps.skills.urls')),
]
