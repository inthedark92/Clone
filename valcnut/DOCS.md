# Valcnut MMORPG - Документация (Django Edition)

## 1. Структура проекта
Проект построен на базе Django с использованием Django REST Framework для API и Django Channels для WebSockets.

- `valcnut/`: Настройки проекта (settings.py, asgi.py, urls.py).
- `apps/`: Приложения игры.
  - `users/`: Пользователи, роли, аутентификация.
  - `characters/`: Персонажи, статы, прогрессия.
  - `battles/`: Боевая система, логика боя, WebSockets.
  - `items/`: Предметы, инвентарь.
  - `core/`: Кланы, банки, рынок.
- `frontend/`: HTML шаблоны.
- `static/`: CSS/JS файлы.

## 2. Быстрый запуск
Для запуска выполните:
```bash
cd valcnut
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 3. Боевая система
Реализована в `apps/battles/engine.py`. Включает расчет урона на основе характеристик:
- Зоны удара (Голова, Тело, Пояс, Ноги).
- Шанс уклонения и блокирования.
- Критические удары.
- Учет брони и типа оружия.

## 4. WebSockets
Используются Django Channels. Подключение по адресу:
`ws://localhost:8000/ws/battle/<character_id>/`

## 5. Админка
Доступна по адресу `http://localhost:8000/admin/`. Позволяет:
- Редактировать статы игроков.
- Создавать предметы.
- Управлять банами.
