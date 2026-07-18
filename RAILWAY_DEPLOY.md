# Railway + PostgreSQL deploy

## Nega ma'lumot o'chmaydi?

Bot kodi va PostgreSQL ikki alohida Railway service bo'ladi. GitHub'ga yangi kod
push qilinganda faqat bot service qayta quriladi. Ma'lumotlar Postgres service
ichida qoladi. Kod startda `CREATE TABLE IF NOT EXISTS` va xavfsiz `ALTER TABLE`
buyruqlarini bajaradi; jadvalni o'chirmaydi.

## Railway sozlamalari

1. GitHub repository'dan bot service yarating.
2. Shu project ichida `+ New` -> `Database` -> `Add PostgreSQL` ni tanlang.
3. Bot service'ni oching -> `Variables`.
4. Quyidagilarni kiriting:
   - `BOT_TOKEN` = BotFather tokeni
   - `OWNER_ID` = Telegram raqamli ID
   - `DATABASE_URL` = Postgres service'ning `DATABASE_URL` reference'i
5. Reference qiymati odatda `${{Postgres.DATABASE_URL}}` ko'rinishida bo'ladi.
   Service nomi boshqa bo'lsa, Railway'dagi `Add Reference` tugmasidan tanlang.
6. Bot service'ni deploy/redeploy qiling.
7. Logda quyidagi yozuv chiqishi kerak:
   `✅ PostgreSQL ulandi; jadvallar saqlandi va tekshirildi`

## Muhim

- PostgreSQL service'ni yoki uning volume'ini o'chirmang.
- `DATABASE_URL` o'rniga `DATABASE_PUBLIC_URL` ishlatmang; service reference afzal.
- `.env` va bot tokenini GitHub'ga push qilmang.
- GitHub yangilanishi Postgres ma'lumotlarini o'chirmaydi.
- Qo'shimcha himoya uchun Postgres volume backups'ni yoqing.

## Tekshirish

1. Botga test kirim kiriting.
2. Railway bot service'da `Redeploy` bosing.
3. Bot qayta ishga tushgach oylik hisobot yoki Excel orqali yozuv qolganini tekshiring.
