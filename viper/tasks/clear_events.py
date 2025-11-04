from viper.cores.core_locks import task_lock


def clear_events():
    if not task_lock.acquire(blocking=False):
        return
    try:
        ...
    finally:
        if task_lock.owned():
            task_lock.release()
