from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InventoryItem, Item, CommissionItem
import random

@login_required
def inventory_view(request):
    items = InventoryItem.objects.filter(user=request.user)
    return render(request, 'game/inventory.html', {'items': items})

@login_required
def market_view(request):
    items = Item.objects.all()
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)

    return render(request, 'game/locations/market.html', {
        'items': items,
        'categories': Item.CATEGORY_CHOICES
    })

@login_required
def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user = request.user

    if user.silver < item.price_silver:
        messages.error(request, "Недостаточно серебра.")
    else:
        user.silver -= item.price_silver
        user.save()
        InventoryItem.objects.create(user=user, item=item)
        messages.success(request, f"Вы купили {item.name}.")

    return redirect('market')

@login_required
def commission_shop_view(request):
    comm_items = CommissionItem.objects.all()
    return render(request, 'game/locations/commission.html', {'items': comm_items})

@login_required
def list_on_commission(request, inv_item_id):
    inv_item = get_object_or_404(InventoryItem, id=inv_item_id, user=request.user)
    if request.method == 'POST':
        price = int(request.POST.get('price', 0))
        if price <= 0:
            messages.error(request, "Цена должна быть больше нуля.")
        else:
            CommissionItem.objects.create(seller=request.user, inventory_item=inv_item, price_silver=price)
            messages.success(request, f"Предмет {inv_item.item.name} выставлен на продажу.")
            return redirect('inventory')

    return render(request, 'game/list_commission.html', {'item': inv_item})

@login_required
def buy_commission_item(request, comm_item_id):
    comm_item = get_object_or_404(CommissionItem, id=comm_item_id)
    user = request.user

    if user == comm_item.seller:
        messages.error(request, "Вы не можете купить свой собственный предмет.")
    elif user.silver < comm_item.price_silver:
        messages.error(request, "Недостаточно серебра.")
    else:
        # Transfer money
        comm_item.seller.silver += comm_item.price_silver
        comm_item.seller.save()

        user.silver -= comm_item.price_silver
        user.save()

        # Transfer item
        inv_item = comm_item.inventory_item
        inv_item.user = user
        inv_item.save()

        comm_item.delete()
        messages.success(request, f"Вы купили {inv_item.item.name} у {comm_item.seller.username}.")

    return redirect('commission_shop')

@login_required
def repair_item(request, item_id):
    inv_item = get_object_or_404(InventoryItem, id=item_id, user=request.user)
    if inv_item.durability_current == 0:
        messages.info(request, "Предмет не нуждается в починке.")
        return redirect('inventory')

    repair_cost = inv_item.durability_current * 2 # 2 silver per 1 point of wear
    if request.user.silver < repair_cost:
        messages.error(request, f"Недостаточно серебра для починки (нужно {repair_cost}).")
        return redirect('inventory')

    request.user.silver -= repair_cost
    request.user.save()
    inv_item.durability_current = 0
    inv_item.save()

    messages.success(request, f"Предмет {inv_item.item.name} успешно починен за {repair_cost} серебра.")
    return redirect('inventory')

ENHANCEMENT_CHANCES = {
    0: 1.0, 1: 0.9, 2: 0.8, 3: 0.7, 4: 0.6, 5: 0.5, 6: 0.4, 7: 0.3,
    8: 0.25, 9: 0.2, 10: 0.15, 11: 0.12, 12: 0.1, 13: 0.08, 14: 0.05, 15: 0.03
}

@login_required
def enhance_item(request, item_id):
    inv_item = get_object_or_404(InventoryItem, id=item_id, user=request.user)
    if inv_item.enhancement_level >= 16:
        messages.warning(request, "Максимальный уровень улучшения достигнут.")
        return redirect('inventory')

    cost = (inv_item.enhancement_level + 1) * 100
    diamond_cost = 1 if inv_item.enhancement_level >= 5 else 0

    if request.user.silver < cost:
        messages.error(request, f"Недостаточно серебра для улучшения (нужно {cost}).")
        return redirect('inventory')
    if request.user.diamonds < diamond_cost:
        messages.error(request, f"Недостаточно алмазов (нужно {diamond_cost}).")
        return redirect('inventory')

    request.user.silver -= cost
    request.user.diamonds -= diamond_cost
    request.user.save()

    chance = ENHANCEMENT_CHANCES.get(inv_item.enhancement_level, 0.01)
    if random.random() < chance:
        inv_item.enhancement_level += 1
        inv_item.save()
        messages.success(request, f"Успех! Предмет {inv_item.item.name} теперь +{inv_item.enhancement_level}!")
    else:
        if inv_item.enhancement_level > 0:
            inv_item.enhancement_level -= 1
            inv_item.save()
            messages.error(request, f"Неудача! Уровень улучшения предмета {inv_item.item.name} снизился до +{inv_item.enhancement_level}.")
        else:
            messages.error(request, f"Неудача! Не удалось улучшить предмет {inv_item.item.name}.")

    return redirect('inventory')
