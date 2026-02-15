import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from apps.battles.consumers import BattleConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'valcnut.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/battle/<int:user_id>/", BattleConsumer.as_asgi()),
        ])
    ),
})
