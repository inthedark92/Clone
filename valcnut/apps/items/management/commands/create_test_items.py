from django.core.management.base import BaseCommand
from apps.items.models import Item

class Command(BaseCommand):
    help = 'Создает тестовые предметы по 1 серебру'

    def handle(self, *args, **kwargs):
        # Очистить старые тестовые предметы (опционально, но лучше просто добавить)

        test_data = [
            # Оружие
            {'name': 'Тестовый Меч', 'item_type': 'weapon', 'category': 'equipment', 'price_silver': 1, 'bonus_min_dmg': 5, 'bonus_max_dmg': 10},
            {'name': 'Тестовый Лук', 'item_type': 'weapon', 'category': 'equipment', 'price_silver': 1, 'bonus_min_dmg': 4, 'bonus_max_dmg': 12},

            # Броня
            {'name': 'Тестовый Доспех', 'item_type': 'armor', 'category': 'equipment', 'price_silver': 1, 'bonus_armor': 10},
            {'name': 'Тестовый Шлем', 'item_type': 'helmet', 'category': 'equipment', 'price_silver': 1, 'bonus_armor': 5},
            {'name': 'Тестовые Сапоги', 'item_type': 'boots', 'category': 'equipment', 'price_silver': 1, 'bonus_agility': 2},

            # Аксессуары
            {'name': 'Тестовое Кольцо', 'item_type': 'ring', 'category': 'equipment', 'price_silver': 1, 'bonus_intuition': 3},
            {'name': 'Тестовый Амулет', 'item_type': 'amulet', 'category': 'equipment', 'price_silver': 1, 'bonus_strength': 2},

            # Эликсиры и еда (Таверна)
            {'name': 'Скандинавский Суп', 'item_type': 'potion', 'category': 'elixirs', 'price_silver': 1, 'restore_hp': 20, 'description': 'category:first Вкусный суп.'},
            {'name': 'Жареное Мясо', 'item_type': 'potion', 'category': 'elixirs', 'price_silver': 1, 'restore_hp': 40, 'description': 'category:second Сочное мясо.'},
            {'name': 'Медовуха', 'item_type': 'potion', 'category': 'elixirs', 'price_silver': 1, 'restore_mp': 30, 'description': 'category:drinks Крепкий напиток.'},

            # Свитки, Квесты, Подарки
            {'name': 'Тестовый Свиток', 'item_type': 'scroll', 'category': 'scrolls', 'price_silver': 1},
            {'name': 'Тестовый Квестовый Предмет', 'item_type': 'quest', 'category': 'quest', 'price_silver': 1},
            {'name': 'Тестовый Подарок', 'item_type': 'gift', 'category': 'gifts', 'price_silver': 1},
        ]

        for data in test_data:
            Item.objects.update_or_create(name=data['name'], defaults=data)
            self.stdout.write(self.style.SUCCESS(f"Создан предмет: {data['name']}"))
