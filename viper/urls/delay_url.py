from starlette.routing import Router

from viper.views import delay_view

delay_url = Router()

delay_url.add_route('/delay-long-task', delay_view.index, ['GET', 'POST'])
