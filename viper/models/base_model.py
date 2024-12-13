from viper.utils.db_util import db


class BaseModel:

    def __init__(self):
        self._conn = None
        self.cursor = None

    async def conn(self):
        if not self.cursor:
            self._conn = await db.acquire()  # 获取连接
            self.cursor = await self._conn.cursor()  # 获取游标

    async def rollback(self):
        await self._conn.rollback()

    async def close(self):
        try:
            if self.cursor:
                await self.cursor.execute('UNLOCK TABLES;')
                await self.cursor.close()  # 关闭游标
            if self._conn:
                await db.release(self._conn)  # 连接放回连接池
        finally:
            self.cursor = None
            self._conn = None

    async def commit(self):
        try:
            await self._conn.commit()
        except Exception:
            await self.rollback()
            raise

    async def execute(self, sql_str, values=None):
        try:
            await self.cursor.execute(sql_str, values)
        except Exception:
            await self.rollback()
            await self.close()
            raise

    async def executemany(self, sql_str, values=None):
        try:
            await self.cursor.executemany(sql_str, values)    # values is [tuple1, tuple2]
        except Exception:
            await self.rollback()
            await self.close()
            raise
