from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import BankAccount, Deal, DealItem
from apps.items.models import Item, InventoryItem
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
def location_view(request, slug='castle'):
    locations = {
        'castle': {
            'title': 'Древний Замок',
            'template': 'game/locations/castle.html',
            'nav': [('battle_halls', 'Боевые Залы')]
        },
        'battle_halls': {
            'title': 'Боевые Залы',
            'template': 'game/locations/battle_halls.html',
            'nav': [
                ('novice_hall', 'Зал Новичков'),
                ('mage_hall', 'Зал Магов (4+)'),
                ('warrior_hall', 'Зал Воинов (4+)'),
                ('hall_fire', 'Зал Огня (Клан)'),
                ('central_square', 'Выход на Центральную Площадь'),
                ('castle', 'Вернуться в Замок')
            ]
        },
        'novice_hall': {
            'title': 'Зал Новичков',
            'template': 'game/locations/novice_hall.html',
            'nav': [('battle_halls', 'Назад в Боевые Залы')]
        },
        'warrior_hall': {
            'title': 'Зал Воинов',
            'template': 'game/locations/warrior_hall.html',
            'nav': [('battle_halls', 'Назад в Боевые Залы')]
        },
        'mage_hall': {
            'title': 'Зал Магов',
            'template': 'game/locations/mage_hall.html',
            'nav': [('battle_halls', 'Назад в Боевые Залы')]
        },
        'hall_fire': {
            'title': 'Зал Огня',
            'template': 'game/locations/elemental.html',
            'alliance': 'fire',
            'nav': [('battle_halls', 'Назад в Боевые Залы')]
        },

        'central_square': {
            'title': 'Центральная Площадь',
            'template': 'game/locations/square.html',
            'nav': [
                ('street', 'ВВЕРХ на Улицу'),
                ('suburb', 'ВНИЗ в Пригород'),
                ('tavern', 'Таверна'),
                ('market', 'Рынок'),
                ('commission_shop', 'Комиссионка'),
                ('forge', 'Кузница'),
                ('mage_school', 'Школа Магов'),
                ('combat_school', 'Школа Воинов'),
                ('battle_halls', 'В Боевые Залы')
            ]
        },
        'street': {
            'title': 'Улица',
            'template': 'game/locations/street.html',
            'nav': [
                ('bank', 'Банк'),
                ('clan_hall', 'Муниципалитет'),
                ('lottery', 'Лотерея'),
                ('sage_hut', 'Хижина Мудреца'),
                ('obelisk', 'Обелиск'),
                ('central_square', 'Вернуться на Площадь')
            ]
        },
        'suburb': {
            'title': 'Пригород',
            'template': 'game/locations/suburb.html',
            'nav': [
                ('mine', 'Шахта'),
                ('field', 'Поле'),
                ('temple', 'Храм'),
                ('cave', 'Пещера'),
                ('central_square', 'Вернуться на Площадь')
            ]
        },
        'cave': {
            'title': 'Пещера',
            'template': 'game/locations/cave.html',
            'nav': [('suburb', 'Вернуться в Пригород')]
        },

        'tavern': {'title': 'Таверна "У Одина"', 'template': 'game/locations/tavern.html', 'nav': [('central_square', 'Назад')]},
        'market': {'title': 'Рынок', 'template': 'game/locations/market.html', 'nav': [('central_square', 'Назад')]},
        'commission_shop': {'title': 'Комиссионный магазин', 'template': 'game/locations/commission.html', 'nav': [('central_square', 'Назад')]},
        'mage_school': {'title': 'Школа Магов', 'template': 'game/locations/school.html', 'nav': [('central_square', 'Назад')]},
        'combat_school': {'title': 'Школа Воинов', 'template': 'game/locations/school.html', 'nav': [('central_square', 'Назад')]},
        'clan_hall': {'title': 'Зал Кланов', 'template': 'game/locations/clans.html', 'nav': [('street', 'Назад')]},
        'bank': {'title': 'Банк Вальхаллы', 'template': 'game/locations/bank.html', 'nav': [('street', 'Назад')]},
        'forge': {'title': 'Кузница', 'template': 'game/locations/forge.html', 'nav': [('central_square', 'Назад')]},
        'mine': {'title': 'Шахта', 'template': 'game/locations/mine.html', 'nav': [('suburb', 'Назад')]},
        'field': {'title': 'Поле', 'template': 'game/locations/field.html', 'nav': [('suburb', 'Назад')]},
        'temple': {'title': 'Храм', 'template': 'game/locations/temple.html', 'nav': [('suburb', 'Назад')]},
        'lottery': {'title': 'Лотерея', 'template': 'game/locations/lottery.html', 'nav': [('street', 'Назад')]},
        'sage_hut': {'title': 'Хижина Мудреца', 'template': 'game/locations/sage.html', 'nav': [('street', 'Назад')]},
        'obelisk': {'title': 'Обелиск', 'template': 'game/locations/obelisk.html', 'nav': [('street', 'Назад')]},
    }

    # Access restrictions
    user = request.user
    if slug == 'clan_hall' and user.level < 7:
        messages.error(request, "Муниципалитет доступен только с 7 уровня.")
        return redirect('location', slug='street')

    if slug == 'novice_hall' and user.level >= 4:
        messages.error(request, "Зал Новичков доступен только до 4 уровня.")
        return redirect('location', slug='battle_halls')

    if slug in ['warrior_hall', 'mage_hall'] and user.level < 4:
        messages.error(request, "Этот зал доступен только с 4 уровня.")
        return redirect('location', slug='battle_halls')

    if slug.startswith('hall_'):
        loc_data = locations.get(slug)
        if not user.clan or user.alliance != loc_data.get('alliance'):
            messages.error(request, f"Доступ в {loc_data['title']} разрешен только членам соответствующего альянса.")
            return redirect('location', slug='battle_halls')

    loc = locations.get(slug, locations['castle'])

    # Update user last location
    if request.user.last_location != slug:
        request.user.last_location = slug
        request.user.save(update_fields=['last_location'])

    return render(request, loc['template'], {
        'title': loc['title'],
        'slug': slug,
        'nav': loc.get('nav', [])
    })

@login_required
def deals_view(request):
    from .models import Deal
    from django.db.models import Q
    deals = Deal.objects.filter(Q(initiator=request.user) | Q(target=request.user)).order_by('-created_at')
    return render(request, 'game/deals.html', {'deals': deals})

@login_required
def map_view(request):
    return render(request, 'game/map.html', {'title': 'Карта Мира'})

@login_required
def mod_panel_view(request):
    if request.user.role not in ['moderator', 'admin']:
        messages.error(request, "У вас нет прав доступа к этой панели.")
        return redirect('game_index')

    User = get_user_model()
    mods = User.objects.filter(role__in=['moderator', 'admin'])
    logs = ChatMessage.objects.all().order_by('-created_at')[:50]

    return render(request, 'game/mod_panel.html', {
        'mods': mods,
        'logs': logs
    })

@login_required
def initiate_deal(request, user_id):
    User = get_user_model()
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        messages.error(request, "Нельзя торговать с самим собой.")
        return redirect('game_index')

    deal = Deal.objects.create(initiator=request.user, target=target)
    return redirect('view_deal', deal_id=deal.id)

@login_required
def view_deal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    if request.user not in [deal.initiator, deal.target]:
        messages.error(request, "У вас нет доступа к этой сделке.")
        return redirect('game_index')

    if deal.status != 'active':
        return render(request, 'game/deal_detail.html', {'deal': deal})

    inventory = request.user.inventory.filter(is_equipped=False)
    # Exclude items already in deal
    deal_item_ids = deal.items.values_list('inventory_item_id', flat=True)
    inventory = inventory.exclude(id__in=deal_item_ids)

    return render(request, 'game/deal_detail.html', {'deal': deal, 'inventory': inventory})

@login_required
def deal_update_silver(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    if deal.status != 'active': return redirect('view_deal', deal_id=deal.id)

    if request.method == 'POST':
        amount = int(request.POST.get('silver', 0))
        if amount < 0: amount = 0

        if request.user == deal.initiator:
            if request.user.silver >= amount:
                deal.initiator_silver = amount
            else:
                messages.error(request, "Недостаточно серебра.")
        elif request.user == deal.target:
            if request.user.silver >= amount:
                deal.target_silver = amount
            else:
                messages.error(request, "Недостаточно серебра.")

        deal.initiator_accepted = False
        deal.target_accepted = False
        deal.save()

    return redirect('view_deal', deal_id=deal.id)

@login_required
def deal_add_item(request, deal_id, item_id):
    deal = get_object_or_404(Deal, id=deal_id)
    inv_item = get_object_or_404(InventoryItem, id=item_id, user=request.user)

    if deal.status == 'active' and (request.user == deal.initiator or request.user == deal.target):
        DealItem.objects.get_or_create(deal=deal, inventory_item=inv_item, owner=request.user)
        deal.initiator_accepted = False
        deal.target_accepted = False
        deal.save()

    return redirect('view_deal', deal_id=deal.id)

@login_required
def deal_remove_item(request, deal_id, deal_item_id):
    deal = get_object_or_404(Deal, id=deal_id)
    deal_item = get_object_or_404(DealItem, id=deal_item_id, owner=request.user)

    if deal.status == 'active':
        deal_item.delete()
        deal.initiator_accepted = False
        deal.target_accepted = False
        deal.save()

    return redirect('view_deal', deal_id=deal.id)

@login_required
def deal_accept(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    if deal.status != 'active': return redirect('view_deal', deal_id=deal.id)

    if request.user == deal.initiator:
        deal.initiator_accepted = True
    elif request.user == deal.target:
        deal.target_accepted = True
    deal.save()

    if deal.initiator_accepted and deal.target_accepted:
        # Final validation
        if deal.initiator.silver < deal.initiator_silver or deal.target.silver < deal.target_silver:
            messages.error(request, "Недостаточно средств у одной из сторон.")
            deal.initiator_accepted = False
            deal.target_accepted = False
            deal.save()
            return redirect('view_deal', deal_id=deal.id)

        # Transfer money
        deal.initiator.silver -= deal.initiator_silver
        deal.initiator.silver += deal.target_silver
        deal.target.silver -= deal.target_silver
        deal.target.silver += deal.initiator_silver
        deal.initiator.save()
        deal.target.save()

        # Transfer items
        for di in deal.items.all():
            di.inventory_item.user = deal.target if di.owner == deal.initiator else deal.initiator
            di.inventory_item.save()

        deal.status = 'accepted'
        deal.save()
        messages.success(request, "Сделка успешно завершена!")
        return redirect('deals')

    return redirect('view_deal', deal_id=deal.id)

@login_required
def deal_cancel(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)
    if request.user in [deal.initiator, deal.target]:
        deal.status = 'cancelled'
        deal.save()
        messages.info(request, "Сделка отменена.")
    return redirect('deals')
