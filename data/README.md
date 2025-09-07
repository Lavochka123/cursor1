# Svety

Цифровые открытки: Telegram-бот + Flask-сайт.

## Быстрый старт
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=...  # или .env
python -m svety.bot.main       # бот
gunicorn -w 2 -b 127.0.0.1:5000 svety.web:app  # веб
