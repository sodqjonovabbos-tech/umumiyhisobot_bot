# Umumiy hisobot Telegram boti

Kirim, chiqim va qarzlarni yuritadigan shaxsiy Telegram bot.

## Railway uchun tayyor

- PostgreSQL (`asyncpg`) bilan ishlaydi.
- Railway'da `DATABASE_URL` ulanmasa SQLite'ga yashirincha o'tmaydi — aniq xato beradi.
- GitHub push/redeploy vaqtida jadvallar o'chirilmaydi.
- Startda faqat mavjud bo'lmagan jadvallar, ustunlar va indekslar qo'shiladi.
- `.env`, lokal SQLite va eksport fayllari GitHub'dan himoyalangan.

To'liq yo'riqnoma: `RAILWAY_DEPLOY.md`.

## Railway variables

```text
BOT_TOKEN=Telegram BotFather tokeni
OWNER_ID=Telegram raqamli ID
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

`DATABASE_URL` qiymatini qo'lda yozish o'rniga Railway `Add Reference` orqali
Postgres service'dan tanlash tavsiya qilinadi.
