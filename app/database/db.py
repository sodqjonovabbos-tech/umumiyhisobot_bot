from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from config import DATABASE_URL
from app.database.models import Base

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    """Railway/PostgreSQL va lokal SQLite uchun jadvallarni ishonchli yaratadi."""
    # 1) Avval asosiy jadvallarni yaratamiz
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2) PostgreSQL eski bazalar uchun xavfsiz migratsiya.
    # Muhim: har bir ALTER alohida transactionda ishlaydi, aks holda bitta xato
    # butun transactionni rollback qilib, jadvallar yaratilmay qolishi mumkin.
    if DATABASE_URL.startswith("postgresql+asyncpg://"):
        postgres_sql = [
            "ALTER TABLE IF EXISTS debts ADD COLUMN IF NOT EXISTS debt_type VARCHAR(20) DEFAULT 'oldim'",
            "ALTER TABLE IF EXISTS debts ADD COLUMN IF NOT EXISTS person VARCHAR(150) DEFAULT ''",
            "ALTER TABLE IF EXISTS incomes ALTER COLUMN amount TYPE BIGINT",
            "ALTER TABLE IF EXISTS expenses ALTER COLUMN amount TYPE BIGINT",
            "ALTER TABLE IF EXISTS debts ALTER COLUMN total_amount TYPE BIGINT",
            "ALTER TABLE IF EXISTS debt_payments ALTER COLUMN amount TYPE BIGINT",
        ]
        for sql in postgres_sql:
            try:
                async with engine.begin() as conn:
                    await conn.execute(text(sql))
            except Exception as e:
                print(f"⚠️ Migration o'tkazib yuborildi: {e}")

    # 3) Yakuniy tekshiruv: yana bir marta create_all chaqiramiz
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
