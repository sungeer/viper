from starlette.routing import Mount

from viper.urls import chat_url, user_url

register_routes = [
    Mount('/chat', app=chat_url.chat_url),
    Mount('/user', app=user_url.user_url)
]
