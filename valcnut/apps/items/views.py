from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InventoryItem
import random

@login_required
def inventory_view(request):
    items = InventoryItem.objects.filter(user=request.user)
    return render(request, 'game/inventory.html', {'items': items})

@login_required
def repair_item(request, item_id):
    inv_item = get_object_or_404(InventoryItem, id=item_id, user=request.user)
    if inv_item.durability_current == inv_item.durability_max:
        messages.info(request, "Предмет не нуждается в починке.")
        return redirect('inventory')

    repair_cost = (inv_item.durability_max - inv_item.durability_current) * 2 # 2 silver per 1 durability
    if request.user.silver < repair_cost:
        messages.error(request, f"Недостаточно серебра для починки (нужно {repair_cost}).")
        return redirect('inventory')

    request.user.silver -= repair_cost
    request.user.save()
    inv_item.durability_current = inv_item.durability_max
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

    cost = (inv_item.enhancement_level + 1) * 100 # Example cost: 100, 200, ... silver
    if request.user.silver < cost:
        messages.error(request, f"Недостаточно серебра для улучшения (нужно {cost}).")
        return redirect('inventory')

    request.user.silver -= cost
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
