#!/usr/bin/env python3
"""Пример использования gloow_sdk"""

from gloow_sdk import GloowClient

# Инициализация
client = GloowClient(session_token="YOUR_SESSION_TOKEN")

# Проверка авторизации
if client.is_authenticated():
    me, err = client.me()
    if me:
        print(f"Авторизован как: {me['user']['handle']}")
    
    # Получить список треков
    tracks, err = client.tracks.list(limit=5)
    print(f"\nНайдено треков: {len(tracks)}")
    for track in tracks:
        print(f"  - {track.title} by {track.author.name}")
    
    # Получить комнаты
    rooms, err = client.rooms.list()
    print(f"\nКомнат: {len(rooms)}")
    for room in rooms:
        print(f"  - {room.name} ({room.visibility})")
    
    # Друзья
    friends, err = client.friends.list()
    print(f"\nДрузей: {len(friends.get('friends', []))}")
    
    # Уведомления
    notifications, err = client.notifications.list()
    print(f"Уведомлений: {len(notifications)}")
else:
    print("Не авторизован. Проверь токен.")
