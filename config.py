import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv

# Railway variables doimo ustun turadi. Lokal .env faqat mavjud bo'lmagan
# qiymatlarni to'ldiradi.
load_dotenv(override=False)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OWNER_ID = int(os.getenv("OWNER_ID", "0") or 0)

IS_RAILWAY = bool(
    os.getenv("RAILWAY_ENVIRONMENT")
    or os.getenv("RAILWAY_PROJECT_ID")
    or os.getenv("RAILWAY_SERVICE_ID")
)


def normalize_database_url(raw_url: str) -> str:
    """Railway PostgreSQL URL manzilini SQLAlchemy asyncpg formatiga o'tkazadi."""
    url = (raw_url or "").strip()

    if url.startswith("postgres://"):
        url = "postgresql+asyncpg://" + url[len("postgres://"):]
    elif url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://"):]
    elif url.startswith("postgresql+psycopg://"):
        url = "postgresql+asyncpg://" + url[len("postgresql+psycopg://"):]

    # DATABASE_PUBLIC_URL ishlatilgan hollarda ayrim provayderlar sslmode
    # parametrini beradi. asyncpg uchun uni ssl parametriga aylantiramiz.
    if url.startswith("postgresql+asyncpg://") and "sslmode=" in url:
        parts = urlsplit(url)
        query_items = []
        for key, value in parse_qsl(parts.query, keep_blank_values=True):
            query_items.append(("ssl" if key == "sslmode" else key, value))
        url = urlunsplit(
            (parts.scheme, parts.netloc, parts.path, urlencode(query_items), parts.fragment)
        )

    return url


_raw_database_url = os.getenv("DATABASE_URL", "").strip()

# Railway'da SQLite ishlatish xavfli: yangi deployda konteyner fayllari
# almashishi mumkin. Shuning uchun PostgreSQL ulanmagan bo'lsa darhol to'xtaydi.
if not _raw_database_url:
    if IS_RAILWAY:
        raise RuntimeError(
            "Railway'da DATABASE_URL topilmadi. Bot servisining Variables "
            "bo'limiga Postgres servisidan DATABASE_URL reference qo'shing."
        )
    _raw_database_url = "sqlite+aiosqlite:///finance.db"

DATABASE_URL = normalize_database_url(_raw_database_url)
DATABASE_KIND = "postgresql" if DATABASE_URL.startswith("postgresql+asyncpg://") else "sqlite"

if IS_RAILWAY and DATABASE_KIND != "postgresql":
    raise RuntimeError(
        "Railway'da SQLite ishlatish bloklandi. DATABASE_URL qiymatini "
        "${{Postgres.DATABASE_URL}} reference orqali PostgreSQL'ga ulang."
    )

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN yozilmagan")
if not OWNER_ID:
    raise RuntimeError("OWNER_ID yozilmagan yoki 0 ga teng")
