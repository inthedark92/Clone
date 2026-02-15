from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.views import RegisterView
from apps.characters.views import CharacterDetailView, CharacterCreateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
    path('api/auth/register', RegisterView.as_view(), name='register'),
    path('api/auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/character/me', CharacterDetailView.as_view(), name='character_me'),
    path('api/character/create', CharacterCreateView.as_view(), name='character_create'),
    # Battles API would go here
]
