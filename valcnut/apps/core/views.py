from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random

@login_required
def extract_resource(request):
    if request.method != 'POST':
        return redirect('location', slug='mine')

    user = request.user
    # Simple extraction logic
    roll = random.random()
    if roll < 0.7:
        silver_gain = random.randint(10, 50)
        user.silver += silver_gain
        messages.success(request, f"Вы добыли {silver_gain} серебра!")
    elif roll < 0.9:
        diamonds_gain = random.randint(1, 3)
        user.diamonds += diamonds_gain
        messages.success(request, f"Вы нашли {diamonds_gain} алмазов!")
    else:
        messages.warning(request, "Вы ничего не нашли в этой жиле.")

    user.save()
    return redirect('location', slug='mine')

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
        'forge': {'title': 'Кузница', 'template': 'game/locations/forge.html'},
        'mine': {'title': 'Шахта', 'template': 'game/locations/mine.html'},
    }

    # Access restrictions
    if slug == 'clan_hall' and request.user.level < 7:
        messages.error(request, "Зал Кланов доступен только с 7 уровня.")
        return redirect('location', slug='central_square')

    loc = locations.get(slug, locations['central_square'])

    # Update user last location
    if request.user.last_location != slug:
        request.user.last_location = slug
        request.user.save(update_fields=['last_location'])

    return render(request, loc['template'], {
        'title': loc['title'],
        'slug': slug
    })
