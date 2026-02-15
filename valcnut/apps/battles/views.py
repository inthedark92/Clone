from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Battle, BattleParticipant
from .monsters import get_monster_for_level

@login_required
def start_pve(request):
    if request.method != 'POST':
        return redirect('location', slug='forest')

    user = request.user
    monster = get_monster_for_level(user.level)

    battle = Battle.objects.create(battle_type='pve', status='in_progress')

    # Player participant
    BattleParticipant.objects.create(
        battle=battle,
        user=user,
        team=1,
        hp_snapshot=user.current_hp,
        stats_snapshot=user.get_battle_stats()
    )

    # Monster participant
    BattleParticipant.objects.create(
        battle=battle,
        npc_id=monster['id'],
        team=2,
        hp_snapshot=monster['hp'],
        stats_snapshot=monster
    )

    # Redirect to battle UI (assuming it exists or will be implemented)
    # Since the prompt doesn't ask for a new battle UI, I'll assume there's one at /ws/battle/
    # But usually there is a template.
    # For now I'll just redirect to forest and maybe they can see battle status?
    # Actually, I'll check if there is a battle view in the codebase.
    return redirect('game_index') # Placeholder
