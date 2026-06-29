from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from config import DATABASE_URL
from app.database.models import Base

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Eski SQLite/PostgreSQL bazada debts jadvali yaratilgan bo'lsa,
        # yangi ustunlarni qo'shib qo'yadi. Xato bo'lsa o'tkazib yuboradi.
        for sql in [
            "ALTER TABLE debts ADD COLUMN debt_type VARCHAR(20) DEFAULT 'oldim'",
            "ALTER TABLE debts ADD COLUMN person VARCHAR(150) DEFAULT ''",
        ]:
            try:
                await conn.execute(text(sql))
            except Exception:
                pass
