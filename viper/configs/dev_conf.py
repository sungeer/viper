from viper.configs.base_conf import BaseSettings


class DevSettings(BaseSettings):
    env = 'dev'

    jwt_secret_key = '91tf6f2f0bbb237143782736075b2t8d48bbacf6aafd6bee609be561d773db36'

    # mysql
    db_name = 'vrm'
    db_port = 3306
    db_user = 'vrm'
    db_pass = '0O/sAR0HvuBCglze1Sg5ZQ=='
    db_host = 'rm-uf6x1fd8n8493j0iw.mysql.rds.aliyuncs.com'

    db_pool_size = 1
    db_max_overflow = 10

    httpx_pool_size = 20
    httpx_max_overflow = 100

    # redis
    redis_host = 'r-uf6kpl6xhzk3371ukp.redis.rds.aliyuncs.com'
    redis_pass = 'GgE0/514s01efLf8mwTfY7btiWRe+73OXu+iF5T1yig='
    redis_port = 6379
    redis_db = 82
