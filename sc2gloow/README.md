# sc2gloow

Инструмент для переноса треков из SoundCloud на [Gloowroom](https://gloowroom.com). Скачивает аудио и обложки, загружает на Gloowroom.

## Возможности

- Перенос одного трека
- Перенос целого плейлиста/альбома
- Скачивание и загрузка обложки
- Поддержка M4A/MP3/WAV/FLAC/OGG
- Автоматические повторы и обработка ошибок
- Встроенный [gloow_sdk](gloow_sdk/) для работы с Gloowroom API
- Итоговый отчёт по загрузкам

## Структура проекта

```
sc2gloow/
├── sc2gloow.py              # Точка входа
├── gloow_sdk/               # Python SDK для Gloowroom API
│   ├── client.py            # GloowClient
│   ├── auth/                # Аутентификация
│   ├── models/              # Модели данных
│   ├── resources/           # API ресурсы
│   └── utils/               # Утилиты
├── config/
│   ├── config.json          # Токены (в .gitignore)
│   └── config.example.json  # Шаблон конфига
├── sc2gloow/
│   ├── sdk/
│   │   └── soundcloud/      # SDK для SoundCloud (yt-dlp)
│   └── utils/
│       └── config.py        # Загрузка конфига
├── requirements.txt
├── .gitignore
└── README.md
```

## Установка

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/shalavochkk/sc2gloow.git
   cd sc2gloow
   ```

2. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Установить ffmpeg (нужен для yt-dlp):
   - Windows: `winget install ffmpeg` или скачать с https://ffmpeg.org
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

4. Настроить конфиг:
   ```bash
   cp config/config.example.json config/config.json
   ```
   Открыть `config/config.json` и добавить токен `__Secure-better-auth.session_token` с gloowroom.com

## Получение токена Gloowroom

1. Зайти на [gloowroom.com](https://gloowroom.com) и авторизоваться
2. Открыть DevTools (F12) → Application → Cookies
3. Найти `__Secure-better-auth.session_token` и скопировать значение

## Использование

### Один трек
```bash
python sc2gloow.py https://soundcloud.com/artist/track-name
```

### Плейлист / Альбом
```bash
python sc2gloow.py https://soundcloud.com/artist/sets/album-name
```

### Свой конфиг
```bash
python sc2gloow.py https://soundcloud.com/artist/track --config my_config.json
```

## Gloowroom SDK

Можно использовать `gloow_sdk` отдельно для работы с API gloowroom.com:

```python
from gloow_sdk import GloowClient

client = GloowClient(session_token="your_token")

# Получить профиль
me, err = client.me()

# Получить треки
tracks, err = client.tracks.list()

# Загрузить трек
track, err = client.tracks.upload(
    audio_path="track.m4a",
    title="Мой трек",
    description="Описание",
    cover_path="cover.jpg"
)
print(f"Загружен: https://gloowroom.com/tracks/{track.slug}")

# Комнаты, друзья, уведомления
rooms, err = client.rooms.list()
friends, err = client.friends.list()
notifications, err = client.notifications.list()
```

Подробная документация в [gloow_sdk/README.md](gloow_sdk/README.md)

## Как это работает

1. **Извлечение** — yt-dlp получает метаданные трека/плейлиста
2. **Скачивание** — аудио + обложка в временную папку
3. **Создание трека** — через gloow_sdk создаётся запись на Gloowroom
4. **Загрузка аудио** — загрузка файла по presigned URL
5. **Загрузка обложки** — загрузка обложки трека
6. **Обработка** — ожидание статуса `ready`

## Требования

- Python 3.8+
- ffmpeg
- requests
- yt-dlp

## Лицензия

MIT
