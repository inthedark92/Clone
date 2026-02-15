import pytest
from ..domain.battle.engine import BattleEngine, HitZone, BattleResultType
from ..domain.battle.logic import BattleLogic
from ..models.battle import Battle, BattleParticipant, BattleStatus

def test_calculate_damage_hit():
    attacker_stats = {'strength': 10, 'min_dmg': 5, 'max_dmg': 10, 'intuition': 0}
    defender_stats = {'agility': 0, 'armor': 0}

    # Hit zone NOT in block zones
    res = BattleEngine.calculate_damage(attacker_stats, defender_stats, HitZone.HEAD, [HitZone.BODY, HitZone.BELT])

    assert res['type'] in [BattleResultType.HIT, BattleResultType.CRIT]
    assert res['damage'] >= 15 # (5+10) to (10+10)

def test_calculate_damage_dodge():
    # High agility should result in some dodges
    attacker_stats = {'strength': 10, 'min_dmg': 5, 'max_dmg': 10, 'intuition': 0}
    defender_stats = {'agility': 100, 'armor': 0} # 100 agility = very high dodge

    dodges = 0
    for _ in range(100):
        res = BattleEngine.calculate_damage(attacker_stats, defender_stats, HitZone.HEAD, [HitZone.BODY])
        if res['type'] == BattleResultType.DODGE:
            dodges += 1

    assert dodges > 0

def test_battle_logic_turn():
    battle = Battle(id=1, current_turn=1)
    p1 = BattleParticipant(character_id=1, hp_snapshot=100, stats_snapshot={'strength': 5, 'min_dmg': 5, 'max_dmg': 5, 'intuition': 0})
    p2 = BattleParticipant(character_id=2, hp_snapshot=100, stats_snapshot={'strength': 5, 'min_dmg': 5, 'max_dmg': 5, 'intuition': 0})

    logic = BattleLogic(battle, [p1, p2])

    actions = {
        1: {"attack": HitZone.HEAD, "blocks": [HitZone.BODY, HitZone.BELT]},
        2: {"attack": HitZone.BODY, "blocks": [HitZone.HEAD, HitZone.BELT]}
    }

    logs = logic.process_turn(actions)

    assert len(logs) >= 2
    assert battle.current_turn == 2
    # p1 attacked HEAD, p2 blocked HEAD -> P1 hit on P2 might be blocked
    # p2 attacked BODY, p1 blocked BODY -> P2 hit on P1 might be blocked
