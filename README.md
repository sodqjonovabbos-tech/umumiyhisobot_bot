# Finance Control Bot

Railway fix:
- PostgreSQL jadvallari startda majburiy yaratiladi
- amount maydonlari BIGINT
- Telegram polling conflict kamaytirish uchun webhook/pending updates tozalanadi
- Dockerfile qo'shildi, Railway mise xatosini aylanib o'tadi

Qarzlar bo'limi:
- "Qarz oldim" orqali kimdan va qancha qarz olingani saqlanadi.
- "Qarz berdim" orqali qarz mavjud odam tanlanib, qaytarilgan summa yoziladi.
- To'liq yopilgan qarz faol ro'yxatdan yashiriladi, lekin Excel tarixida saqlanadi.
- Qarz Excel faylida qarz olish, birovga berilgan eski qarzlar va qarz qaytarishlar alohida varaqlarda chiqadi.
