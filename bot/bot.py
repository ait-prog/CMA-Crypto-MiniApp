import os
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загружаем переменные окружения из .env файла
try:
    from dotenv import load_dotenv
    # Ищем .env файл в корне проекта (на уровень выше)
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    # Если python-dotenv не установлен, используем переменные окружения системы
    pass

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ait-prog.github.io/CMA-Crypto-MiniApp/")  # фронт


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        coin = context.args[0] if context.args else "bitcoin"
        print(f"Получена команда /start от пользователя {update.effective_user.id}")
        
        keyboard = [
            [
                InlineKeyboardButton(
                    "Open App", web_app=WebAppInfo(url=f"{WEBAPP_URL}?coin={coin}")
                )
            ]
        ]
        await update.message.reply_text(
            "Открывай мини-приложение 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        print(f"Ответ отправлен пользователю {update.effective_user.id}")
    except Exception as e:
        print(f"Ошибка при обработке команды /start: {e}")
        try:
            await update.message.reply_text(
                "Произошла ошибка. Попробуйте позже."
            )
        except:
            pass


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не установлен!")
        print("Проверьте файл .env в корне проекта")
        exit(1)
    
    print(f"BOT_TOKEN: {'Установлен' if BOT_TOKEN else 'Не установлен'}")
    print(f"WEBAPP_URL: {WEBAPP_URL}")
    print("Инициализация бота...")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Бот запущен и готов к работе!")
    print("Ожидание команд...")
    app.run_polling()

