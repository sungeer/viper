from viper.cores.core_redis import redis_conn


task_lock = redis_conn.lock('task_lock', timeout=60)
