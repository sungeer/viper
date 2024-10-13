import redis.asyncio as redis

from viper.configs import settings
from viper.utils.cipher import cipher


def redis_conn(host=settings.redis_host, port=6379, db=0, decode_responses=False):
    return redis.Redis(
        host=host,
        port=port,
        db=db,
        password=settings.redis_pass,  # password=cipher.decrypt(settings.redis_pass),
        decode_responses=decode_responses
    )


redis_client = redis_conn(decode_responses=True)


async def close_redis():
    await redis_client.aclose()
