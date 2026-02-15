from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Battle, BattleParticipant
from .monsters import get_monster_for_level
import random

@login_required
def start_pve(request):
    if request.method != 'POST':
        return redirect('location', slug='forest')

    user = request.user
    monster = get_monster_for_level(user.level)

    # Simple simulated battle result
    # In a real game, this would be turn-based, but here we process it for the hunt
    win_chance = 0.7 + (user.level * 0.05)
    if random.random() < win_chance:
        # Success
        gold_gain = random.randint(monster['gold_min'], monster['gold_max'])
        exp_gain = monster['exp']
        user.silver += gold_gain # Using silver for gold rewards for now
        user.monster_wins += 1
        user.add_exp(exp_gain)
        messages.success(request, f"Победа над {monster['name']}! Получено: {gold_gain} серебра, {exp_gain} опыта.")
    else:
        # Loss
        user.monster_losses += 1
        user.current_hp = max(1, user.current_hp * 0.5)
        user.save()
        messages.error(request, f"Вы проиграли в схватке с {monster['name']}.")

    # Durability loss (accumulation of wear)
    equipped = user.inventory.filter(is_equipped=True)
    for item in equipped:
        item.durability_current = min(item.durability_max, item.durability_current + random.randint(1, 3))
        item.save()

    return redirect('location', slug='forest')

@login_required
def start_duel(request):
    if request.user.last_location != 'arena':
        messages.error(request, "Дуэли возможны только на Арене.")
        return redirect('location', slug=request.user.last_location)

    # Placeholder for duel search or direct challenge
    messages.info(request, "Поиск противника для дуэли...")
    return redirect('location', slug='arena')
