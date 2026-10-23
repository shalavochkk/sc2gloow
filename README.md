# sc2gloow

Инструмент для переноса треков из SoundCloud на [Gloowroom](https://gloowroom.com). Скачивает аудио (с обложкой) из SoundCloud и загружает на Gloowroom.

## Возможности

- Перенос одного трека
- Перенос целого плейлиста/альбома
- Скачивание и загрузка обложки
- Поддержка M4A/MP3/WAV/FLAC/OGG
- Автоматические повторы и обработка ошибок
- Итоговый отчёт по загрузкам
- SDK для Gloowroom API (можно использовать отдельно)

## Структура проекта

```
sc2gloow/
├── sc2gloow.py              # Точка входа
├── config/
│   ├── config.json          # Токены (в .gitignore)
│   └── config.example.json  # Шаблон конфига
├── sc2gloow/
│   ├── sdk/
│   │   ├── gloowroom/       # SDK для Gloowroom API
│   │   │   └── client.py    # GloowroomClient
│   │   └── soundcloud/      # SDK для SoundCloud
│   │       └── downloader.py # SoundCloudDownloader
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
   Открыть `config/config.json` и заполнить токены (см. ниже).

## Получение токенов

### Gloowroom Session Token
1. Зайти на [gloowroom.com](https://gloowroom.com) и авторизоваться
2. Открыть DevTools (F12) → Application → Cookies
3. Найти `__Secure-better-auth.session_token` и скопировать значение

### SoundCloud (необязательно)
Большинство публичных треков работают без токена. Для приватных треков может понадобиться OAuth-токен.

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

### Своя папка для скачивания
```bash
python sc2gloow.py https://soundcloud.com/artist/track --output-dir /tmp/downloads
```

## Как это работает

1. **Извлечение** — yt-dlp получает метаданные и ссылки на скачивание
2. **Скачивание** — аудио (M4A/MP3) + обложка в временную папку
3. **Создание трека** — `POST /api/tracks` на Gloowroom
4. **Загрузка аудио** — `PUT` на полученный upload URL
5. **Загрузка обложки** — `PUT /api/tracks/{id}/cover`
6. **Обработка** — ожидание статуса `ready` на Gloowroom

## SDK

### GloowroomClient
```python
from sc2gloow.sdk.gloowroom import GloowroomClient

client = GloowroomClient(session_token="your_token")
track_id, url, err = client.upload_track_full(
    audio_path="track.m4a",
    title="My Track",
    description="Description",
    cover_path="cover.jpg"
)
```

### SoundCloudDownloader
```python
from sc2gloow.sdk.soundcloud import SoundCloudDownloader

dl = SoundCloudDownloader(output_dir="./downloads")
tracks, album = dl.extract_track_list("https://soundcloud.com/artist/sets/album")
audio, cover, title, desc = dl.download(tracks[0]["url"])
```

## Требования

- Python 3.8+
- ffmpeg
- requests
- yt-dlp

## Лицензия

MIT
