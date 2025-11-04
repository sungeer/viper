from viper.cores.core_redis import redis_conn


task_lock = redis_conn.lock(
    'task_lock',
    timeout=60,  # 持有 锁 的最大时间 秒
    blocking=False  # 拿不到锁 则立即放弃
)
