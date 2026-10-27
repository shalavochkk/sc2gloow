# gloow_sdk

Профессиональный Python SDK для [Gloowroom](https://gloowroom.com) API.

## Установка

```bash
# Скопируй папку gloow_sdk в свой проект или установи
pip install requests
```

## Быстрый старт

```python
from gloow_sdk import GloowClient

# Инициализация с токеном сессии
client = GloowClient(session_token="your_session_token")

# Проверка авторизации
if client.is_authenticated():
    me, err = client.me()
    print(me)
```

## Получение токена

1. Зайди на [gloowroom.com](https://gloowroom.com) и авторизуйся
2. Открой DevTools (F12) → Application → Cookies
3. Скопируй значение `__Secure-better-auth.session_token`

## Возможности

### Аутентификация
```python
# Получить сессию
session = client.get_session()

# Получить текущего пользователя
me, err = client.me()
```

### Треки
```python
# Список треков
tracks, err = client.tracks.list(limit=20, offset=0)

# Получить трек
track, err = client.tracks.get("track_id")

# Загрузить трек (полный цикл)
track, err = client.tracks.upload(
    audio_path="track.m4a",
    title="Название трека",
    description="Описание",
    cover_path="cover.jpg",
    explicit=False,
    genre="drill"
)

# Удалить трек
success, msg = client.tracks.delete("track_id")
```

### Пользователи
```python
# Получить пользователя по хэндлу
user_data, err = client.users.get("username")

# Получить треки пользователя
tracks, err = client.users.get_tracks("username")
```

### Комнаты
```python
# Список комнат
rooms, err = client.rooms.list()

# Детали комнаты
room, err = client.rooms.get("room_id")
```

### Друзья
```python
# Список друзей
friends, err = client.friends.list()

# Запросы в друзья
requests, err = client.friends.get_requests()
```

### Уведомления
```python
# Список уведомлений
notifications, err = client.notifications.list()
```

## Структура

```
gloow_sdk/
├── __init__.py          # Точка входа
├── client.py            # GloowClient
├── auth/                # Аутентификация
├── client/              # HTTP клиент
├── endpoints/           # Определения эндпоинтов
├── models/              # Модели данных (Track, User, Room)
├── resources/           # API ресурсы (tracks, users, rooms, friends)
└── utils/               # Утилиты (HTTP клиент)
```

## API эндпоинты

| Метод | Эндпоинт | Описание |
|---|---|---|
| GET | `/api/auth/get-session` | Получить сессию |
| GET | `/api/me` | Текущий пользователь |
| GET | `/api/tracks` | Список треков |
| POST | `/api/tracks` | Создать трек |
| GET | `/api/tracks/{id}` | Получить трек |
| DELETE | `/api/tracks/{id}` | Удалить трек |
| PUT | `/api/tracks/{id}/cover` | Загрузить обложку |
| GET | `/api/users/{handle}` | Профиль пользователя |
| GET | `/api/rooms` | Список комнат |
| GET | `/api/rooms/{id}` | Детали комнаты |
| GET | `/api/friends` | Список друзей |
| GET | `/api/friends/requests` | Запросы в друзья |
| GET | `/api/notifications` | Уведомления |

## Пример использования

```python
from gloow_sdk import GloowClient

client = GloowClient(session_token="YOUR_TOKEN")

# Получить профиль
user, err = client.users.get("shalavochka")
print(f"Пользователь: {user['user']['name']}")
print(f"Треков: {len(user['tracks'])}")

# Загрузить трек
track, err = client.tracks.upload(
    audio_path="music.mp3",
    title="Мой трек",
    cover_path="cover.jpg"
)
if track:
    print(f"Загружен: https://gloowroom.com/tracks/{track.slug}")
```

## Лицензия

MIT
