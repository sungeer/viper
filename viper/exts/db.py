import aiomysql

from touch.configs import settings
from touch.utils.cipher import cipher


class BaseDB:
    _pool = None

    @classmethod
    async def connect(cls):
        if cls._pool is None:
            cls._pool = await aiomysql.create_pool(
                host=settings.db_host,
                port=settings.db_port,
                db=settings.db_name,
                user=settings.db_user,
                password=cipher.decrypt(settings.db_pass),
                minsize=settings.db_pool_size,
                maxsize=settings.db_max_overflow,
                pool_recycle=3600,
                charset='utf8mb4',
                cursorclass=aiomysql.DictCursor
            )
        return cls._pool

    @classmethod
    async def disconnect(cls):
        if cls._pool is not None:
            cls._pool.close()
            await cls._pool.wait_closed()
            cls._pool = None

    @property
    def pool(self):
        return self.__class__._pool


db = BaseDB()


async def creat_db_pool():
    if db.pool is None:
        await db.connect()
    return db.pool
