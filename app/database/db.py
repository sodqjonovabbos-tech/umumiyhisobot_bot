from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DATABASE_KIND, DATABASE_URL
from app.database.models import Base

engine_options = {
    "echo": False,
    "pool_pre_ping": True,
}

# PostgreSQL ulanishlarini uzoq ishlaydigan Telegram bot uchun barqaror saqlaydi.
if DATABASE_KIND == "postgresql":
    engine_options.update(
        pool_recycle=1800,
        pool_size=5,
        max_overflow=5,
    )

engine = create_async_engine(DATABASE_URL, **engine_options)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Bu migratsiyalar faqat mavjud bo'lmagan jadval/ustunlarni qo'shadi.
# DROP TABLE yoki eski ma'lumotlarni o'chiradigan buyruq yo'q.
CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS incomes (
        id SERIAL PRIMARY KEY,
        amount BIGINT NOT NULL,
        source VARCHAR(120) NOT NULL,
        note TEXT DEFAULT '',
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id SERIAL PRIMARY KEY,
        amount BIGINT NOT NULL,
        category VARCHAR(120) NOT NULL,
        note TEXT DEFAULT '',
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS debts (
        id SERIAL PRIMARY KEY,
        debt_type VARCHAR(20) DEFAULT 'oldim',
        person VARCHAR(150) DEFAULT '',
        name VARCHAR(150) NOT NULL,
        total_amount BIGINT NOT NULL,
        note TEXT DEFAULT '',
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS debt_payments (
        id SERIAL PRIMARY KEY,
        debt_id INTEGER REFERENCES debts(id) ON DELETE CASCADE,
        amount BIGINT NOT NULL,
        note TEXT DEFAULT '',
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
    )
    """,
]

POSTGRES_SAFE_MIGRATIONS = [
    "ALTER TABLE IF EXISTS debts ADD COLUMN IF NOT EXISTS debt_type VARCHAR(20) DEFAULT 'oldim'",
    "ALTER TABLE IF EXISTS debts ADD COLUMN IF NOT EXISTS person VARCHAR(150) DEFAULT ''",
    "ALTER TABLE IF EXISTS incomes ALTER COLUMN amount TYPE BIGINT",
    "ALTER TABLE IF EXISTS expenses ALTER COLUMN amount TYPE BIGINT",
    "ALTER TABLE IF EXISTS debts ALTER COLUMN total_amount TYPE BIGINT",
    "ALTER TABLE IF EXISTS debt_payments ALTER COLUMN amount TYPE BIGINT",
    "CREATE INDEX IF NOT EXISTS ix_incomes_created_at ON incomes (created_at)",
    "CREATE INDEX IF NOT EXISTS ix_expenses_created_at ON expenses (created_at)",
    "CREATE INDEX IF NOT EXISTS ix_debts_created_at ON debts (created_at)",
    "CREATE INDEX IF NOT EXISTS ix_debt_payments_debt_id ON debt_payments (debt_id)",
]


async def init_db():
    """Bazani tekshiradi; mavjud ma'lumotlarni hech qachon o'chirmaydi."""
    if DATABASE_KIND == "postgresql":
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
            for sql in CREATE_TABLES_SQL:
                await conn.execute(text(sql))
            for sql in POSTGRES_SAFE_MIGRATIONS:
                await conn.execute(text(sql))
        print("✅ PostgreSQL ulandi; jadvallar saqlandi va tekshirildi")
        return

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Lokal SQLite jadvallari tekshirildi")
