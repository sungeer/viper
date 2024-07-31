import httpx

from touch.configs import settings

limits = httpx.Limits(
    max_keepalive_connections=settings.httpx_pool_size,
    max_connections=settings.httpx_max_overflow
)

timeout = httpx.Timeout(
    connect=2.0,
    read=5.0,
    write=2.0,
    pool=2.0
)

httpx_client = httpx.AsyncClient(limits=limits, timeout=timeout)


async def close_httpx():
    await httpx_client.aclose()
