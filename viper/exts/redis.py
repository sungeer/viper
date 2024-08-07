import redis.asyncio as redis

from viper.configs import settings
from viper.utils.cipher import cipher

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    password=cipher.decrypt(settings.redis_pass),
    decode_responses=True
)
