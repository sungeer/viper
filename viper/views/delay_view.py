from viper.utils.resp_util import jsonify
from viper.delays.backgrounds import delay_long_task


async def index(request):
    await delay_long_task()
    message = {'message': 'Long-running task has been started!'}
    return jsonify(message)
