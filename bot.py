
import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("YOUR_TOKEN")
WEBHOOK_PATH = "/telegram"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

products = {
    "Jacket/Skirt": [("Комплект с шерстью", "https://chat.openai.com/mnt/data/jacket_skirt.jpeg", 1200000)],
    "Suit": [("Тёмный костюм", "https://chat.openai.com/mnt/data/suit.jpeg", 1500000)],
    "Dress": [("Трикотажное платье", "https://chat.openai.com/mnt/data/dress.jpeg", 950000)],
}

app_bot = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"cat:{cat}")] for cat in products]
    await update.message.reply_text("Добро пожаловать в Nepovtorimo Bot! Выберите категорию:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat = query.data.split(":")[1]
    for name, photo, price in products[cat]:
        keyboard = [[InlineKeyboardButton("Купить", callback_data=f"buy:{name}")]]
        await query.message.reply_photo(photo=photo, caption=f"{name}\nЦена: {price:,} RUB", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Ваш заказ принят. Менеджер свяжется с вами в ближайшее время.")

app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CallbackQueryHandler(handle_category, pattern="^cat:"))
app_bot.add_handler(CallbackQueryHandler(handle_purchase, pattern="^buy:"))

fastapi_app = FastAPI()

@fastapi_app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, app_bot.bot)
    await app_bot.process_update(update)
    return {"ok": True}

# Устойчивый запуск без post_init
async def set_webhook_and_run():
    await app_bot.initialize()
    await app_bot.bot.set_webhook(WEBHOOK_URL)
    await app_bot.start()

import asyncio
asyncio.get_event_loop().create_task(set_webhook_and_run())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot:fastapi_app", host="0.0.0.0", port=10000)
