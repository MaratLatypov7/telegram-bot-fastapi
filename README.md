
# Telegram Bot Store (FastAPI + Webhook)

## Что внутри:
- Бот с FastAPI
- Категории: Suit, Dress, Jacket/Skirt
- Webhook поддержка через Render

## Развёртывание на Render:

**Start command**:
uvicorn bot:fastapi_app --host 0.0.0.0 --port 10000

**Environment variables**:
YOUR_TOKEN = (токен от @BotFather)
WEBHOOK_URL = https://<your-app>.onrender.com/telegram

**Зависимости**: хранятся в requirements.txt
