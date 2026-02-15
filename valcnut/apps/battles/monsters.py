import random

MONSTER_POOL = {
    0: [
        {'id': 'weak_wolf_0', 'name': 'Слабый волк', 'level': 0, 'hp': 40, 'strength': 2, 'agility': 2, 'intuition': 2, 'gold_min': 5, 'gold_max': 10, 'exp': 20},
    ],
    1: [
        {'id': 'weak_wolf_1', 'name': 'Слабый волк', 'level': 1, 'hp': 50, 'strength': 3, 'agility': 3, 'intuition': 3, 'gold_min': 7, 'gold_max': 15, 'exp': 30},
    ],
    2: [
        {'id': 'wild_boar_2', 'name': 'Дикий кабан', 'level': 2, 'hp': 80, 'strength': 5, 'agility': 4, 'intuition': 3, 'gold_min': 15, 'gold_max': 25, 'exp': 50},
    ],
    3: [
        {'id': 'wild_boar_3', 'name': 'Дикий кабан', 'level': 3, 'hp': 100, 'strength': 6, 'agility': 5, 'intuition': 4, 'gold_min': 20, 'gold_max': 35, 'exp': 70},
    ],
    4: [
        {'id': 'dark_raider_4', 'name': 'Темный рейдер', 'level': 4, 'hp': 150, 'strength': 8, 'agility': 7, 'intuition': 6, 'gold_min': 40, 'gold_max': 60, 'exp': 120},
    ],
    5: [
        {'id': 'dark_raider_5', 'name': 'Темный рейдер', 'level': 5, 'hp': 180, 'strength': 10, 'agility': 9, 'intuition': 8, 'gold_min': 50, 'gold_max': 80, 'exp': 150},
    ],
}

def get_monster_for_level(level):
    if level in MONSTER_POOL:
        return random.choice(MONSTER_POOL[level])

    available_levels = sorted(MONSTER_POOL.keys(), reverse=True)
    for l in available_levels:
        if level >= l:
            return random.choice(MONSTER_POOL[l])
    return MONSTER_POOL[0][0]
