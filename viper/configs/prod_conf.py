from viper.configs.base_conf import BaseSettings


class ProdSettings(BaseSettings):
    env = 'prod'

    # mysql
    db_name = 'viper'
    db_port = 3306
    db_host = '127.0.0.1'

    # redis
    redis_host = '127.0.0.1'

    db_pool_size = 5
    db_max_overflow = 10

    httpx_pool_size = 10
    httpx_max_overflow = 100

    stream_pool_size = 10
    stream_max_overflow = 100
