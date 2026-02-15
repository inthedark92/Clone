from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankAccount
from apps.items.models import Item
import random

@login_required
def bank_view(request):
    bank, created = BankAccount.objects.get_or_create(user=request.user)
    return render(request, 'game/locations/bank.html', {
        'bank': bank,
        'title': 'Банк Вальхаллы'
    })

@login_required
def bank_deposit(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        currency = request.POST.get('currency', 'silver')
        bank, created = BankAccount.objects.get_or_create(user=request.user)

        if amount <= 0:
            messages.error(request, "Сумма должна быть больше нуля.")
        elif currency == 'silver':
            if request.user.silver >= amount:
                request.user.silver -= amount
                bank.balance_silver += amount
                request.user.save()
                bank.save()
                messages.success(request, f"Вы внесли {amount} серебра на счет.")
            else:
                messages.error(request, "Недостаточно серебра.")
        elif currency == 'gold':
            if request.user.gold >= amount:
                request.user.gold -= amount
                bank.balance_gold += amount
                request.user.save()
                bank.save()
                messages.success(request, f"Вы внесли {amount} золота на счет.")
            else:
                messages.error(request, "Недостаточно золота.")

    return redirect('bank')

@login_required
def bank_withdraw(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        currency = request.POST.get('currency', 'silver')
        bank, created = BankAccount.objects.get_or_create(user=request.user)

        if amount <= 0:
            messages.error(request, "Сумма должна быть больше нуля.")
        elif currency == 'silver':
            if bank.balance_silver >= amount:
                bank.balance_silver -= amount
                request.user.silver += amount
                bank.save()
                request.user.save()
                messages.success(request, f"Вы сняли {amount} серебра со счета.")
            else:
                messages.error(request, "Недостаточно серебра на банковском счету.")
        elif currency == 'gold':
            if bank.balance_gold >= amount:
                bank.balance_gold -= amount
                request.user.gold += amount
                bank.save()
                request.user.save()
                messages.success(request, f"Вы сняли {amount} золота со счета.")
            else:
                messages.error(request, "Недостаточно золота на банковском счету.")

    return redirect('bank')

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
def tavern_view(request):
    category = request.GET.get('category', 'first')
    # Filter items by custom tavern categories
    items = Item.objects.filter(category='elixirs', description__icontains=f"category:{category}")

    categories = [
        ('first', 'Первые блюда'),
        ('second', 'Вторые блюда'),
        ('third', 'Третьи блюда'),
        ('salads', 'Салаты'),
        ('drinks', 'Напитки'),
    ]

    return render(request, 'game/locations/tavern.html', {
        'items': items,
        'categories': categories,
        'current_category': category,
        'title': 'Таверна "У Одина"'
    })

@login_required
def tavern_buy(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            messages.error(request, "Количество должно быть больше нуля.")
            return redirect('tavern')

        item = get_object_or_404(Item, id=item_id)
        total_cost = item.price_silver * quantity

        if request.user.silver >= total_cost:
            request.user.silver -= total_cost

            # Restore HP/MP
            restore_hp = item.restore_hp * quantity
            restore_mp = item.restore_mp * quantity

            request.user.current_hp = min(request.user.max_hp, request.user.current_hp + restore_hp)
            request.user.current_mp = min(request.user.max_mp, request.user.current_mp + restore_mp)

            request.user.save()
            messages.success(request, f"Вы купили и употребили {item.name} ({quantity} шт.). Восстановлено {restore_hp} HP и {restore_mp} MP.")
        else:
            messages.error(request, "Недостаточно серебра.")

    return redirect('tavern')

@login_required
def location_view(request, slug='novice_hall'):
    locations = {
        # Combat Halls
        'novice_hall': {'title': 'Зал Новичков', 'template': 'game/locations/novice_hall.html'},
        'warrior_hall': {'title': 'Зал Воинов', 'template': 'game/locations/warrior_hall.html'},
        'mage_hall': {'title': 'Зал Магов', 'template': 'game/locations/mage_hall.html'},

        # Elemental Halls
        'hall_fire': {'title': 'Зал Огня', 'template': 'game/locations/elemental.html', 'alliance': 'fire'},
        'hall_water': {'title': 'Зал Воды', 'template': 'game/locations/elemental.html', 'alliance': 'water'},
        'hall_air': {'title': 'Зал Воздуха', 'template': 'game/locations/elemental.html', 'alliance': 'air'},
        'hall_earth': {'title': 'Зал Земли', 'template': 'game/locations/elemental.html', 'alliance': 'earth'},
        'hall_light': {'title': 'Зал Света', 'template': 'game/locations/elemental.html', 'alliance': 'light'},
        'hall_dark': {'title': 'Зал Тьмы', 'template': 'game/locations/elemental.html', 'alliance': 'dark'},

        # Main City
        'central_square': {'title': 'Центральная Площадь', 'template': 'game/locations/square.html'},
        'arena': {'title': 'Арена', 'template': 'game/locations/arena.html'},
        'tavern': {'title': 'Таверна "У Одина"', 'template': 'game/locations/tavern.html'},
        'market': {'title': 'Рынок', 'template': 'game/locations/market.html'},
        'commission_shop': {'title': 'Комиссионный магазин', 'template': 'game/locations/commission.html'},
        'mage_school': {'title': 'Школа Магов', 'template': 'game/locations/school.html'},
        'combat_school': {'title': 'Школа Воинов', 'template': 'game/locations/school.html'},
        'clan_hall': {'title': 'Зал Кланов', 'template': 'game/locations/clans.html'},
        'forest': {'title': 'Темный Лес', 'template': 'game/locations/forest.html'},
        'bank': {'title': 'Банк Вальхаллы', 'template': 'game/locations/bank.html'},
        'forge': {'title': 'Кузница', 'template': 'game/locations/forge.html'},

        # Suburb
        'suburb': {'title': 'Пригород', 'template': 'game/locations/suburb.html'},
        'mine': {'title': 'Шахта', 'template': 'game/locations/mine.html'},
        'field': {'title': 'Поле', 'template': 'game/locations/field.html'},
        'temple': {'title': 'Храм', 'template': 'game/locations/temple.html'},
        'cave': {'title': 'Пещера', 'template': 'game/locations/cave.html'},
        'sub_cave': {'title': 'Подземелье', 'template': 'game/locations/sub_cave.html'},
    }

    # Access restrictions
    user = request.user
    if slug == 'clan_hall' and user.level < 7:
        messages.error(request, "Зал Кланов доступен только с 7 уровня.")
        return redirect('location', slug='central_square')

    if slug == 'novice_hall' and user.level >= 4:
        messages.error(request, "Зал Новичков доступен только до 4 уровня.")
        return redirect('location', slug='central_square')

    if slug in ['warrior_hall', 'mage_hall'] and user.level < 4:
        messages.error(request, "Этот зал доступен только с 4 уровня.")
        return redirect('location', slug='novice_hall')

    if slug.startswith('hall_'):
        loc_data = locations.get(slug)
        if not user.clan or user.alliance != loc_data.get('alliance'):
            messages.error(request, f"Доступ в {loc_data['title']} разрешен только членам соответствующего альянса.")
            return redirect('location', slug='novice_hall' if user.level < 4 else 'central_square')

    loc = locations.get(slug, locations['central_square'])

    # Update user last location
    if request.user.last_location != slug:
        request.user.last_location = slug
        request.user.save(update_fields=['last_location'])

    return render(request, loc['template'], {
        'title': loc['title'],
        'slug': slug
    })
