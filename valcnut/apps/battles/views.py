from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Battle, BattleParticipant
from .monsters import get_monster_for_level
from django.utils import timezone
import random

@login_required
def start_pve(request):
    if request.method != 'POST':
        return redirect('location', slug='forest')

    user = request.user
    # Check if already in battle
    existing = Battle.objects.filter(participants__user=user, status='in_progress').first()
    if existing:
        return redirect('combat', battle_id=existing.id)

    monster_data = get_monster_for_level(user.level)

    # Create Battle
    battle = Battle.objects.create(battle_type='pve', status='in_progress')

    # Add Player
    BattleParticipant.objects.create(
        battle=battle, user=user, team=1,
        hp_snapshot=user.current_hp,
        stats_snapshot=user.get_battle_stats()
    )

    # Add Monster
    BattleParticipant.objects.create(
        battle=battle, npc_id=monster_data['id'], team=2,
        hp_snapshot=monster_data['hp'],
        stats_snapshot=monster_data
    )

    return redirect('combat', battle_id=battle.id)

@login_required
def combat_view(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    player_part = battle.participants.get(user=request.user)

    if battle.status == 'finished':
        return render(request, 'game/combat_result.html', {
            'battle': battle,
            'player': player_part
        })

    monster_part = battle.participants.exclude(user=request.user).first()

    return render(request, 'game/combat.html', {
        'battle': battle,
        'player': player_part,
        'monster': monster_part
    })

@login_required
def combat_turn(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    if battle.status != 'in_progress' or request.method != 'POST':
        return redirect('game_index')

    hit_zone = request.POST.get('hit')
    block_zone = request.POST.get('block')

    player_part = battle.participants.get(user=request.user)
    monster_part = battle.participants.exclude(user=request.user).first()

    # Simple Turn Logic
    # 1. Player attacks Monster
    monster_hit = random.choice(['head', 'body', 'belt', 'legs'])
    damage_to_monster = random.randint(player_part.stats_snapshot['min_dmg'], player_part.stats_snapshot['max_dmg'])

    # 2. Monster attacks Player
    monster_attack_zone = random.choice(['head', 'body', 'belt', 'legs'])
    damage_to_player = random.randint(monster_part.stats_snapshot['strength'], monster_part.stats_snapshot['strength']*2)

    if block_zone == monster_attack_zone:
        damage_to_player = 0
        p_log = f"Вы заблокировали удар в {block_zone}!"
    else:
        player_part.hp_snapshot -= damage_to_player
        p_log = f"Монстр ударил вас в {monster_attack_zone} на {damage_to_player} HP."

    monster_part.hp_snapshot -= damage_to_monster
    m_log = f"Вы ударили монстра в {hit_zone} на {damage_to_monster} HP."

    battle.log.append({'turn': battle.current_turn, 'p': p_log, 'm': m_log})
    battle.current_turn += 1

    # Check for death
    if player_part.hp_snapshot <= 0 or monster_part.hp_snapshot <= 0:
        battle.status = 'finished'
        battle.finished_at = timezone.now()

        if player_part.hp_snapshot > 0:
            player_part.is_winner = True
            # Rewards
            gold_gain = random.randint(monster_part.stats_snapshot['gold_min'], monster_part.stats_snapshot['gold_max'])
            exp_gain = monster_part.stats_snapshot['exp']
            request.user.silver += gold_gain
            request.user.monster_wins += 1
            request.user.add_exp(exp_gain)
            result_msg = f"Победа! Получено {gold_gain} серебра и {exp_gain} опыта."
        else:
            request.user.monster_losses += 1
            request.user.current_hp = 1
            result_msg = "Вы погибли в бою."

        request.user.current_hp = max(0, player_part.hp_snapshot)
        request.user.save()

        # Durability loss
        equipped = request.user.inventory.filter(is_equipped=True)
        for item in equipped:
            item.durability_current = min(item.durability_max, item.durability_current + random.randint(1, 3))
            item.save()

        # Send to system chat
        from apps.core.models import ChatMessage
        ChatMessage.objects.create(user=request.user, text=result_msg, channel='system')

    player_part.save()
    monster_part.save()
    battle.save()

    return redirect('combat', battle_id=battle.id)

@login_required
def start_duel(request):
    if request.user.last_location != 'arena':
        messages.error(request, "Дуэли возможны только на Арене.")
        return redirect('location', slug=request.user.last_location)

    # Placeholder for duel search or direct challenge
    messages.info(request, "Поиск противника для дуэли...")
    return redirect('location', slug='arena')
