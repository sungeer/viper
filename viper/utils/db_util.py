import MySQLdb
from MySQLdb.cursors import DictCursor
from dbutils.pooled_db import PooledDB

from viper.configs import settings

dbpool = PooledDB(
    creator=MySQLdb,
    maxcached=5,
    host=settings.db_host,
    port=settings.db_port,
    db=settings.db_name,
    user=settings.db_user,
    passwd=settings.db_pass,
    charset='utf8',
    cursorclass=DictCursor
)


def create_dbconn():
    conn = dbpool.connection()  # 从连接池中获取一个连接
    return conn
