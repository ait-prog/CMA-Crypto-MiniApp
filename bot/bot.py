import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-domain.app")  # фронт


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = context.args[0] if context.args else "bitcoin"
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


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не установлен!")
        exit(1)
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Бот запущен...")
    app.run_polling()

