import random
from enum import IntEnum
from typing import List, Dict, Optional, Tuple

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
    def calculate_damage(
        attacker_stats: Dict,
        defender_stats: Dict,
        hit_zone: HitZone,
        block_zones: List[HitZone],
        is_offhand: bool = False
    ) -> Dict:
        """
        Calculates the outcome of a single attack.
        """
        # Multipliers for off-hand
        dmg_multiplier = 0.5 if is_offhand else 1.0

        # 1. Check for Dodge
        dodge_chance = (defender_stats.get('agility', 3) * 0.02) - (attacker_stats.get('intuition', 3) * 0.01)
        dodge_chance = max(0.05, min(0.40, dodge_chance)) # Cap dodge between 5% and 40%

        if random.random() < dodge_chance:
            return {"type": BattleResultType.DODGE, "damage": 0}

        # 2. Check for Block
        if hit_zone in block_zones:
            # Shield increases block effectiveness
            has_shield = defender_stats.get('has_shield', False)
            if has_shield or random.random() < 0.5: # 50% chance to fully block if zone matches
                return {"type": BattleResultType.BLOCK, "damage": 0}

        # 3. Check for Parry (if not blocked)
        parry_chance = (defender_stats.get('agility', 3) * 0.01)
        if random.random() < parry_chance:
            return {"type": BattleResultType.PARRY, "damage": 0}

        # 4. Calculate Base Damage
        if is_offhand:
            min_dmg = attacker_stats.get('offhand_min_dmg', 1)
            max_dmg = attacker_stats.get('offhand_max_dmg', 3)
        else:
            min_dmg = attacker_stats.get('min_dmg', 1)
            max_dmg = attacker_stats.get('max_dmg', 5)

        base_dmg = random.randint(min_dmg, max_dmg)

        # Strength bonus: 1 point = +1 damage
        strength_bonus = attacker_stats.get('strength', 3)
        total_dmg = (base_dmg + strength_bonus) * dmg_multiplier

        # 5. Check for Critical Strike
        crit_chance = (attacker_stats.get('intuition', 3) * 0.03)
        is_crit = random.random() < crit_chance

        if is_crit:
            total_dmg *= 2
            result_type = BattleResultType.CRIT
        else:
            result_type = BattleResultType.HIT

        # 6. Armor Reduction
        armor = defender_stats.get('armor', 0)
        # Simple reduction: 5 armor = -1 damage, but at least 1 damage
        reduction = armor // 5
        total_dmg = max(1, total_dmg - reduction)

        return {
            "type": result_type,
            "damage": int(total_dmg),
            "hit_zone": hit_zone
        }
