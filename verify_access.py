import os
import django
import sys

# Set up django environment
sys.path.append('/app/valcnut')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'valcnut.settings')
django.setup()

from django.test import RequestFactory
from apps.core.views import location_view
from apps.users.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

def test_clan_hall_access():
    user = User.objects.get(username='regtest')
    factory = RequestFactory()
    request = factory.get('/game/clan_hall/')
    request.user = user

    # Add messages middleware support
    setattr(request, '_messages', FallbackStorage(request))

    response = location_view(request, slug='clan_hall')

    print(f"Status code: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirected to: {response['Location']}")

    # Check messages
    messages = [m.message for m in request._messages]
    print(f"Messages: {messages}")

if __name__ == "__main__":
    test_clan_hall_access()
