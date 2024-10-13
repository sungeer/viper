from viper.utils.db_util import db


class BaseModel:

    def __init__(self):
        self._conn = None
        self.cursor = None

    async def conn(self):
        if not self.cursor:
            if not self._conn:
                self._conn = await db.acquire()  # 获取连接
            self.cursor = await self._conn.cursor()  # 获取游标

    async def rollback(self):
        if not self._conn:
            raise ValueError('connection is not acquired')
        await self._conn.rollback()

    async def close(self):
        try:
            if self._conn:
                if self.cursor:
                    await self.cursor.execute('UNLOCK TABLES;')
                    await self.cursor.close()  # 关闭游标
                await db.release(self._conn)  # 连接放回连接池
        except Exception as exc:
            raise Exception(f'db close failed:{exc}')
        finally:
            self.cursor = None
            self._conn = None

    async def commit(self):
        try:
            await self._conn.commit()
        except Exception as exc:
            await self.rollback()
            raise Exception(f'db commit failed:{exc}')

    async def execute(self, sql_str, values=None):
        try:
            await self.cursor.execute(sql_str, values)
        except Exception as exc:
            await self.rollback()
            await self.close()
            raise Exception(f'db execute failed:{exc}')

    async def executemany(self, sql_str, values=None):
        try:
            await self.cursor.executemany(sql_str, values)    # values is [tuple1, tuple2]
        except Exception as exc:
            await self.rollback()
            await self.close()
            raise Exception(f'db executemany failed:{exc}')
