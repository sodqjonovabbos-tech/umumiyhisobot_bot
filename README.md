# Finance Control Bot

## Railway xatosi tuzatildi
Agar Railway logda `No module named greenlet` chiqsa, bu ZIPda `requirements.txt` ichiga `greenlet>=3.1.1` qo'shilgan.

## Railway Variables
BOT_TOKEN=BotFather token
OWNER_ID=Telegram ID
DATABASE_URL=${{Postgres.DATABASE_URL}}
TIMEZONE=Asia/Tashkent

## Local ishga tushirish
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env
python main.py
