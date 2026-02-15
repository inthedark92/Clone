# Valcnut MMORPG - Документация

## 1. Инструкции по установке

### Требования
- Docker и Docker Compose
- Python 3.12+ (для локальной разработки без Docker)
- PostgreSQL (для локальной разработки без Docker)

### Запуск через Docker
1. Клонируйте репозиторий.
2. Скопируйте `.env.example` в `.env` и настройте переменные.
3. Выполните команду:
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```
4. API будет доступно по адресу `http://localhost:8000`.
5. Документация Swagger: `http://localhost:8000/docs`.

### Локальная разработка
1. Создайте виртуальное окружение: `python -m venv venv`.
2. Активируйте: `source venv/bin/activate`.
3. Установите зависимости: `pip install -r requirements.txt`.
4. Запустите сервер: `uvicorn app.main:app --reload`.

---

## 2. ER-диаграмма (Описание)

Система использует реляционную базу данных PostgreSQL.

- **User**: Хранит данные для аутентификации (username, email, password_hash, role). Связан с Character (1:N).
- **Character**: Основная сущность игрока (stats: str, agi, int, etc., current_hp/mp, location). Связан с Inventory (1:N).
- **Item**: Шаблоны предметов (name, type, requirements, bonuses).
- **InventoryItem**: Экземпляры предметов у персонажа. Связан с Item (N:1).
- **Battle**: Сущность битвы (status, type, turn_count, log).
- **BattleParticipant**: Связывает персонажа с битвой. Хранит снимок характеристик на начало боя и текущее HP.
- **Clan**: Кланы (name, leader_id).
- **BankAccount**: Банковские счета персонажей.
- **MarketplaceItem**: Выставленные на продажу предметы.

---

## 3. Документация API (Основные эндпоинты)

- `POST /api/v1/auth/register`: Регистрация.
- `POST /api/v1/auth/login`: Получение JWT токена.
- `GET /api/v1/character/me`: Получение данных своего персонажа.
- `POST /api/v1/battle/challenge/{id}`: Вызов игрока на бой.
- `POST /api/v1/battle/{id}/turn`: Отправка хода (зона удара и зоны блока).
- `GET /api/v1/admin/character/{id}/stats`: (Admin) Редактирование характеристик.

---

## 4. Обзор безопасности

- **Аутентификация**: Используется JWT (JSON Web Tokens) с алгоритмом HS256. Пароли хешируются с помощью `bcrypt`.
- **Авторизация**: Ролевая модель (Player, Moderator, Admin) проверяется через FastAPI Dependency Injection.
- **Server Authoritative**: Все вычисления (урон, шанс уворота, проверка инвентаря) происходят только на сервере. Клиент отправляет только намерения (действия).
- **Валидация**: Pydantic используется для строгой валидации всех входящих данных.

---

## 5. Масштабируемость

- **Backend**: FastAPI — асинхронный фреймворк, способный обрабатывать тысячи одновременных WebSocket соединений.
- **Stateless API**: Сервер приложений не хранит состояние сессии (кроме WebSocket соединений), что позволяет запускать несколько экземпляров за Load Balancer.
- **WebSockets**: Использование Redis (в планах) для Pub/Sub позволит масштабировать WebSocket-серверы горизонтально.
- **Database**: PostgreSQL с индексами по ключевым полям (username, char_name, battle_id) обеспечивает быструю выборку.
