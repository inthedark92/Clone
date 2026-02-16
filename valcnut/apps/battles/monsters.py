import random

MONSTER_POOL = {
    0: [
        {'id': 'weak_wolf_0', 'name': 'Слабый волк', 'level': 0, 'hp': 40, 'strength': 2, 'agility': 2, 'intuition': 2, 'silver_min': 5, 'silver_max': 10, 'exp_min': 15, 'exp_max': 25},
    ],
    1: [
        {'id': 'weak_wolf_1', 'name': 'Слабый волк', 'level': 1, 'hp': 50, 'strength': 3, 'agility': 3, 'intuition': 3, 'silver_min': 8, 'silver_max': 15, 'exp_min': 25, 'exp_max': 40},
    ],
    2: [
        {'id': 'wild_boar_2', 'name': 'Дикий кабан', 'level': 2, 'hp': 80, 'strength': 5, 'agility': 4, 'intuition': 3, 'silver_min': 15, 'silver_max': 30, 'exp_min': 40, 'exp_max': 60},
    ],
    3: [
        {'id': 'wild_boar_3', 'name': 'Дикий кабан', 'level': 3, 'hp': 100, 'strength': 6, 'agility': 5, 'intuition': 4, 'silver_min': 25, 'silver_max': 45, 'exp_min': 60, 'exp_max': 85},
    ],
    4: [
        {'id': 'dark_raider_4', 'name': 'Темный рейдер', 'level': 4, 'hp': 150, 'strength': 8, 'agility': 7, 'intuition': 6, 'silver_min': 40, 'silver_max': 80, 'exp_min': 100, 'exp_max': 150},
    ],
    5: [
        {'id': 'dark_raider_5', 'name': 'Темный рейдер', 'level': 5, 'hp': 180, 'strength': 10, 'agility': 9, 'intuition': 8, 'silver_min': 60, 'silver_max': 120, 'exp_min': 150, 'exp_max': 220},
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
