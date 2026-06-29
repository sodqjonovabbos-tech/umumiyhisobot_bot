import os
from dotenv import load_dotenv

load_dotenv(override=True)

BOT_TOKEN = os.getenv('BOT_TOKEN', '').strip()
OWNER_ID = int(os.getenv('OWNER_ID', '0') or 0)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///finance.db').strip()

if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)

if not BOT_TOKEN:
    raise RuntimeError('BOT_TOKEN .env ichida yozilmagan')
if not OWNER_ID:
    print('⚠️ OWNER_ID yozilmagan. Hamma foydalanuvchi bloklanadi.')
