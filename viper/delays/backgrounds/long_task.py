import time

from viper.delays.log_config import logger
from viper.delays.huey_instance import huey


@huey.task()
def long_running_task():
    logger.info('Starting long-running task...')
    time.sleep(20)
    logger.info('Long-running task completed!')
