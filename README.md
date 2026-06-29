# Pul oqimini nazorat qilish Telegram bot

## Imkoniyatlar

- Kirim qo'shish
- Chiqim qo'shish
- Qarz oldim
- Qarz berdim
- Qarzlar ro'yxati
- Qarzga to'lov qo'shish
- Qarzdorlik Excel yuklash
- Umumiy Excel eksport
- Kun oxirida avtomatik kunlik Excel hisobot
- Oy oxirida avtomatik oylik Excel hisobot
- Oylik matnli hisobot
- Qidirish
- Faqat OWNER_ID foydalana oladi

## Avtomatik Excel

Bot ishlab turgan bo'lsa:

- Har kuni 23:55 dan keyin kunlik Excel hisobot yuboradi.
- Har oyning oxirgi kuni 23:50 dan keyin oylik Excel hisobot yuboradi.
- Vaqt zonasi: Asia/Tashkent.

Muhim: avtomatik hisobot kelishi uchun bot serverda doim ishlab turishi kerak. Railwayga qo'ysangiz, bot doim ishlaydi.

## Windowsda ishga tushirish

1. ZIPni Desktopga chiqarib oling.

2. PowerShellda papkaga kiring:
```powershell
cd C:\Users\User\Desktop\finance_control_bot
```

3. Virtual muhit yarating:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

4. Kutubxonalarni o'rnating:
```powershell
pip install -r requirements.txt
```

5. `.env` yarating:
```powershell
copy .env.example .env
notepad .env
```

6. `.env` ichiga yozing:
```env
BOT_TOKEN=BotFatherdan_olgan_tokeningiz
OWNER_ID=Telegram_ID_raqamingiz
DATABASE_URL=sqlite+aiosqlite:///finance.db
```

7. Botni ishga tushiring:
```powershell
python main.py
```

## Railway uchun

Railway PostgreSQL qo'shsangiz, `DATABASE_URL` avtomatik chiqadi. Agar Railway URL `postgresql://...` ko'rinishida bo'lsa, bot uni avtomatik `postgresql+asyncpg://...` qilib ishlatadi.

Railway start komandasi:
```bash
python main.py
```
