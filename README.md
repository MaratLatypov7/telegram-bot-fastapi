
# Telegram Bot Store с FastAPI + Webhook

## Что внутри

- FastAPI сервер
- Telegram бот с категориями: Jacket/Skirt, Suit, Dress
- Подключение через Webhook (без polling)

## Установка

1. Установи зависимости:
```bash
pip install -r requirements.txt
```

2. Укажи переменные окружения:
- `YOUR_TOKEN` — токен от @BotFather
- `WEBHOOK_URL` — например: https://your-app-name.onrender.com/telegram

3. Запусти:
```bash
uvicorn bot:fastapi_app --host 0.0.0.0 --port 10000
```

## Для Render

- Start Command: `uvicorn bot:fastapi_app --host 0.0.0.0 --port 10000`
- Environment variables:
  - `YOUR_TOKEN`: токен Telegram
  - `WEBHOOK_URL`: https://your-render-url.onrender.com/telegram
