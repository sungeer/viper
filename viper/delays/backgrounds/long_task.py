import time

from viper.delays.log_config import logger
from viper.delays.huey_instance import huey


@huey.task()
def long_task():
    logger.info('Starting long-running task...')
    time.sleep(3)
    logger.info('Long-running task completed!')
