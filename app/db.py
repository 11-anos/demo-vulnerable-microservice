"""
db.py — Safe async database connection pool.
"""
import asyncpg
from contextlib import asynccontextmanager
from app.config import Settings

settings = Settings()
_pool: asyncpg.Pool | None = None


async def _get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            dsn=settings.database_url,
            min_size=2,
            max_size=10,        # bounded — prevents connection exhaustion
            command_timeout=30,
        )
    return _pool


@asynccontextmanager
async def get_db_connection():
    pool = await _get_pool()
    async with pool.acquire() as conn:
        yield conn


async def close_db_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
