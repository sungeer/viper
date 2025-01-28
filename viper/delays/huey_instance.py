from huey import RedisHuey
from redis import ConnectionPool

from viper.core import settings
from viper.delays.log_config import logger  # noqa 配置日志记录器

redis_pool = ConnectionPool(
    host=settings.CONF.get_conf('REDIS', 'HOST'),
    port=6379,
    # password=settings.CONF.get_int_conf('REDIS', 'PORT'),
    db=0
)

huey = RedisHuey(settings.CONF.get_conf('APP', 'NAME'), connection_pool=redis_pool, blocking=True)

# 在消费者 启动时 加载 定时任务
from viper.delays import schedules  # noqa
