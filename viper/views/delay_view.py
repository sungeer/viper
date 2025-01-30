from viper.utils.resp_util import jsonify
from viper.delays.backgrounds import delay_long_task
from viper.utils.pools import run_in_thread_pool_delay


async def index(request):
    await run_in_thread_pool_delay(delay_long_task)
    message = {'message': 'Long-running task has been started!'}
    return jsonify(message)
