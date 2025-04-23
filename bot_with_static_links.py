
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("YOUR_TOKEN")
WEBHOOK_PATH = "/telegram"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

BASE_URL = os.environ.get("STATIC_BASE_URL") or "https://your-project.onrender.com"

products = {
    "Jacket/Skirt": [("Комплект с шерстью", f"{BASE_URL}/static/jacket_skirt.jpg", 1200000)],
    "Suit": [("Тёмный костюм", f"{BASE_URL}/static/suit.jpg", 1500000)],
    "Dress": [("Трикотажное платье", f"{BASE_URL}/static/dress.jpg", 950000)],
}

app_bot = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"cat:{cat}")] for cat in products]
    await update.message.reply_text("Добро пожаловать в Nepovtorimo Bot! Выберите категорию:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    cat = query.data.split(":")[1]
    items = products.get(cat, [])
    if not items:
        await query.message.reply_text("Категория пока пуста.")
        return

    for name, photo, price in items:
        keyboard = [[InlineKeyboardButton("Купить", callback_data=f"buy:{name}")]]
        try:
            await query.message.reply_photo(
                photo=photo,
                caption=f"{name}\nЦена: {price:,} RUB",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            await query.message.reply_text(f"Ошибка при загрузке товара: {e}")

async def handle_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Ваш заказ принят. Менеджер свяжется с вами в ближайшее время.")

app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CallbackQueryHandler(handle_category, pattern="^cat:"))
app_bot.add_handler(CallbackQueryHandler(handle_purchase, pattern="^buy:"))

fastapi_app = FastAPI()
fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")

@fastapi_app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, app_bot.bot)
    await app_bot.process_update(update)
    return {"ok": True}

async def set_webhook_and_run():
    await app_bot.initialize()
    await app_bot.bot.set_webhook(WEBHOOK_URL)
    await app_bot.start()

import asyncio
asyncio.get_event_loop().create_task(set_webhook_and_run())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:fastapi_app", host="0.0.0.0", port=10000)
