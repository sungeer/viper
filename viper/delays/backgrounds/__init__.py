from viper.delays.backgrounds import long_task


def delay_long_task():
    long_task.long_task.delay()
