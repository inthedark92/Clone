from sqlalchemy.orm import Session
from ..models.character import Character
from ..schemas.character import CharacterCreate, CharacterUpdate
from typing import List, Dict

class CharacterService:
    @staticmethod
    def calculate_stats(character: Character) -> Dict:
        """
        Calculates total stats including bonuses from equipment.
        """
        stats = {
            "strength": character.strength,
            "agility": character.agility,
            "intuition": character.intuition,
            "endurance": character.endurance,
            "intelligence": character.intelligence,
            "wisdom": character.wisdom,
            "spirit": character.spirit,
            "min_dmg": 1,
            "max_dmg": 5,
            "armor": 0,
            "max_hp": character.max_hp,
            "max_mp": character.max_mp,
            "is_dual_wielding": False,
            "has_shield": False
        }

        # Add bonuses from equipped items
        for inv_item in character.inventory:
            if inv_item.is_equipped:
                item = inv_item.item
                stats["strength"] += item.bonus_strength
                stats["agility"] += item.bonus_agility
                stats["intuition"] += item.bonus_intuition
                stats["endurance"] += item.bonus_endurance
                stats["armor"] += item.bonus_armor
                stats["min_dmg"] += item.bonus_min_dmg
                stats["max_dmg"] += item.bonus_max_dmg

                if inv_item.slot == "off_hand":
                    if item.item_type.name == "SHIELD":
                        stats["has_shield"] = True
                    elif item.item_type.name == "WEAPON":
                        stats["is_dual_wielding"] = True
                        stats["offhand_min_dmg"] = item.bonus_min_dmg + 1
                        stats["offhand_max_dmg"] = item.bonus_max_dmg + 3

        # Recalculate HP/MP based on total endurance/wisdom
        stats["max_hp"] = 30 + (stats["endurance"] * 10)
        stats["max_mp"] = 20 + (stats["wisdom"] * 10)

        return stats

    @staticmethod
    def level_up(character: Character, db: Session):
        # Simple exp table: level * 100
        needed_exp = character.level * 100
        if character.exp >= needed_exp:
            character.level += 1
            character.exp -= needed_exp
            character.stat_points += 5
            db.commit()
            db.refresh(character)
            return True
        return False
