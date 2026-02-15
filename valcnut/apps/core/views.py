from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def location_view(request, slug='central_square'):
    locations = {
        'central_square': {'title': 'Центральная Площадь', 'template': 'game/locations/square.html'},
        'arena': {'title': 'Арена', 'template': 'game/locations/arena.html'},
        'tavern': {'title': 'Таверна "У Одина"', 'template': 'game/locations/tavern.html'},
        'market': {'title': 'Рынок', 'template': 'game/locations/market.html'},
        'clan_hall': {'title': 'Зал Кланов', 'template': 'game/locations/clans.html'},
        'forest': {'title': 'Темный Лес', 'template': 'game/locations/forest.html'},
        'bank': {'title': 'Банк Вальхаллы', 'template': 'game/locations/bank.html'},
    }

    loc = locations.get(slug, locations['central_square'])

    # Update user last location
    if request.user.last_location != slug:
        request.user.last_location = slug
        request.user.save(update_fields=['last_location'])

    return render(request, loc['template'], {
        'title': loc['title'],
        'slug': slug
    })
