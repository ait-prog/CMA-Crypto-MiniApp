#!/usr/bin/env python3
"""Тестовый скрипт для проверки подключения бота к Telegram"""

import os
from pathlib import Path
from dotenv import load_dotenv
from telegram import Bot

# Загружаем переменные окружения
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("[ERROR] BOT_TOKEN не найден в .env файле!")
    exit(1)

print(f"[OK] Токен найден (длина: {len(BOT_TOKEN)} символов)")
print("Проверка подключения к Telegram API...")

try:
    import asyncio
    bot = Bot(token=BOT_TOKEN)
    
    async def check_bot():
        bot_info = await bot.get_me()
        print(f"\n[OK] Бот успешно подключен!")
        print(f"   Имя: @{bot_info.username}")
        print(f"   Название: {bot_info.first_name}")
        if bot_info.last_name:
            print(f"   Фамилия: {bot_info.last_name}")
        print(f"\n[OK] Бот готов к работе!")
        print(f"   Отправьте /start боту @{bot_info.username}")
    
    asyncio.run(check_bot())
except Exception as e:
    print(f"\n[ERROR] Ошибка подключения к Telegram:")
    print(f"   {type(e).__name__}: {e}")
    print("\nВозможные причины:")
    print("  1. Неверный BOT_TOKEN")
    print("  2. Проблемы с интернет-соединением")
    print("  3. Telegram API временно недоступен")
    exit(1)

