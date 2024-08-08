import os
import logging
import time
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from datetime import datetime
from queue import Queue

from viper.configs import settings


def initialize_handlers():
    handlers = []
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s | %(process)d | %(module)s.%(funcName)s:%(lineno)d - %(message)s')
    if settings.env not in ('dev',):
        current_date = datetime.now().strftime('%Y%m%d')
        pid = os.getpid()
        log_dir = os.path.join(settings.basedir, f'logs/{settings.app_name}')
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f'{settings.app_name}_{current_date}_{pid}.log')
        fh = RotatingFileHandler(log_file_path, maxBytes=50 * 1024 * 1024, backupCount=3, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        handlers.append(fh)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    handlers.append(console)
    return handlers


def stop_logger():
    while not log_queue.empty():
        time.sleep(0.1)
    queue_listener.stop()


log_queue = Queue(-1)

handlers = initialize_handlers()
queue_listener = QueueListener(log_queue, *handlers)
queue_listener.start()

logger = logging.getLogger(settings.app_name)
logger.setLevel(logging.DEBUG)
queue_handler = QueueHandler(log_queue)
logger.addHandler(queue_handler)
