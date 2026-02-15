import random
from enum import IntEnum

class HitZone(IntEnum):
    HEAD = 1
    BODY = 2
    BELT = 3
    LEGS = 4

class BattleResultType(IntEnum):
    HIT = 1
    CRIT = 2
    BLOCK = 3
    DODGE = 4
    PARRY = 5

class BattleEngine:
    @staticmethod
    def calculate_damage(attacker_stats, defender_stats, hit_zone, block_zones, is_offhand=False):
        dmg_multiplier = 0.5 if is_offhand else 1.0

        # Dodge
        dodge_chance = (defender_stats.get('agility', 3) * 0.02) - (attacker_stats.get('intuition', 3) * 0.01)
        dodge_chance = max(0.05, min(0.40, dodge_chance))
        if random.random() < dodge_chance:
            return {"type": BattleResultType.DODGE, "damage": 0}

        # Block
        if hit_zone in block_zones:
            has_shield = defender_stats.get('has_shield', False)
            if has_shield or random.random() < 0.5:
                return {"type": BattleResultType.BLOCK, "damage": 0}

        # Parry
        parry_chance = (defender_stats.get('agility', 3) * 0.01)
        if random.random() < parry_chance:
            return {"type": BattleResultType.PARRY, "damage": 0}

        # Base Damage
        if is_offhand:
            min_dmg = attacker_stats.get('offhand_min_dmg', 1)
            max_dmg = attacker_stats.get('offhand_max_dmg', 3)
        else:
            min_dmg = attacker_stats.get('min_dmg', 1)
            max_dmg = attacker_stats.get('max_dmg', 5)

        base_dmg = random.randint(min_dmg, max_dmg)
        strength_bonus = attacker_stats.get('strength', 3)
        total_dmg = (base_dmg + strength_bonus) * dmg_multiplier

        # Crit
        crit_chance = (attacker_stats.get('intuition', 3) * 0.03)
        if random.random() < crit_chance:
            total_dmg *= 2
            result_type = BattleResultType.CRIT
        else:
            result_type = BattleResultType.HIT

        # Armor
        armor = defender_stats.get('armor', 0)
        reduction = armor // 5
        total_dmg = max(1, total_dmg - reduction)

        return {
            "type": result_type,
            "damage": int(total_dmg),
            "hit_zone": hit_zone
        }
