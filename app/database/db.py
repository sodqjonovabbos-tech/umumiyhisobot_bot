from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from config import DATABASE_URL
from app.database.models import Base

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

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

async def init_db():
    """PostgreSQL/Railway va lokal SQLite uchun jadvallarni ishonchli yaratadi."""
    if DATABASE_URL.startswith("postgresql+asyncpg://"):
        async with engine.begin() as conn:
            for sql in CREATE_TABLES_SQL:
                await conn.execute(text(sql))
            await conn.execute(text("ALTER TABLE IF EXISTS debts ADD COLUMN IF NOT EXISTS debt_type VARCHAR(20) DEFAULT 'oldim'"))
            await conn.execute(text("ALTER TABLE IF EXISTS debts ADD COLUMN IF NOT EXISTS person VARCHAR(150) DEFAULT ''"))
            await conn.execute(text("ALTER TABLE IF EXISTS incomes ALTER COLUMN amount TYPE BIGINT"))
            await conn.execute(text("ALTER TABLE IF EXISTS expenses ALTER COLUMN amount TYPE BIGINT"))
            await conn.execute(text("ALTER TABLE IF EXISTS debts ALTER COLUMN total_amount TYPE BIGINT"))
            await conn.execute(text("ALTER TABLE IF EXISTS debt_payments ALTER COLUMN amount TYPE BIGINT"))
        print("✅ PostgreSQL jadvallari tekshirildi/yaratildi")
        return

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ SQLite jadvallari tekshirildi/yaratildi")
