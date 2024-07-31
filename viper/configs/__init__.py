import os
from functools import lru_cache

from dotenv import load_dotenv

from viper.configs.dev_conf import DevSettings

config = {
    'dev': DevSettings,
}


@lru_cache()
def get_settings():
    load_dotenv()
    config_name = os.getenv('APP_ENV', 'prod')
    sec_key = os.environ['SEC_KEY']
    configs = config[config_name]()  # oop
    setattr(configs, 'sec_key', sec_key)
    return configs


settings = get_settings()
