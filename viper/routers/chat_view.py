import json

import httpx
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from viper.configs import settings
from viper.utils.http_client import httpx_common, httpx_stream
from viper.utils.tools import jsonify, abort
from viper.utils import jwt_util, tools
from viper.models.chat_model import ChatModel
from viper.models.message_model import MessageModel
from viper.models.content_model import ContentModel
from viper.utils.log_util import logger

route = APIRouter(prefix='/chat')

api_key = settings.ai_api_key
workspace_id = settings.ai_workspace_id
robot_id = settings.ai_robot_id

headers = {
    'Content-Type': 'application/json',
    'Access-key': api_key,
    'Workspace-Id': workspace_id
}


@route.post('/chat-id')
async def get_chat_id(request):
    user_id, error_code = await jwt_util.verify_token(request)
    if not user_id:
        return abort(error_code)

    body = await request.json()
    title = body.get('title')
    if not title:
        return abort(404)

    url = f'{settings.ai_url}/v1/oapi/agent/chat/conversation/create'
    data = {
        'robot_id': robot_id,
        'user': 'wangxun',
        'title': title
    }
    try:
        response = await httpx_common.post(url, headers=headers, json=data)
    except httpx.TimeoutException:
        return abort(504)
    try:
        response = response.json()
    except json.JSONDecodeError:
        return abort(502)
    data = response.get('data')
    if not data:
        return abort(502)
    conversation_id = data.get('conversation_id')
    if not conversation_id:
        return abort(502)
    await ChatModel().add_chat(conversation_id, title, user_id)
    return jsonify(conversation_id)


async def get_response(conversation_id, content):
    url = f'{settings.ai_url}/v1/oapi/agent/chat'
    data = {
        'robot_id': robot_id,
        'conversation_id': conversation_id,
        'content': content,
        'response_mode': 'streaming'
    }
    error_msg = {'finish': 'error'}
    try:
        async with httpx_stream.stream('POST', url=url, headers=headers, json=data) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue
                yield line
    except httpx.TimeoutException:
        logger.error(f'ai time out: 【{conversation_id}】')
        yield f'data: {tools.dict_to_json(error_msg)}\n\n'
    except (Exception,):
        logger.opt(exception=True).error(f'ai error 【{conversation_id}】.')
        yield f'data: {tools.dict_to_json(error_msg)}\n\n'


async def stream_data(conversation_id, chat_id, trace_id, content):
    full_content = []
    async for line in get_response(conversation_id, content):
        answer = line.replace('data: ', '')
        try:
            answer = tools.json_to_dict(answer)
        except json.JSONDecodeError:
            continue
        is_error = answer.get('finish')
        if is_error:
            yield f'{is_error}\n'
            break
        if answer.get('type') == 'TEXT' and answer.get('status') == 'SUCCEEDED':
            content = answer.get('content')
            full_content.append(content)
            yield f'{content}\n'

    content_str = ''.join(full_content) if full_content else 'error'
    message_id = await MessageModel().add_message(chat_id, trace_id, 'robot')
    await ContentModel().add_content(message_id, content_str)


@route.post('/send-message')
async def send_message(request):
    user_id, error_code = await jwt_util.verify_token(request)  # 用户鉴权
    if not user_id:
        return abort(error_code)

    body = await request.json()

    conversation_id = body.get('conversation_id')
    if not conversation_id:
        return abort(400)

    content = body.get('content')
    if not content:
        return abort(400)

    trace_id = tools.generate_uuid()
    chat_info = await ChatModel().get_chat_by_conversation(conversation_id)
    chat_id = chat_info['ID']
    message_id = await MessageModel().add_message(chat_id, trace_id, 'user')
    await ContentModel().add_content(message_id, content)

    return StreamingResponse(stream_data(conversation_id, chat_id, trace_id, content), media_type='text/event-stream')


@route.post('/chats')  # 所有会话
async def get_chats(request):
    user_id, error_code = await jwt_util.verify_token(request)  # 用户鉴权
    if not user_id:
        return abort(error_code)

    chats = await ChatModel().get_chats(user_id)
    return jsonify(chats)


@route.post('/messages')  # 所有问答
async def get_messages(request):
    user_id, error_code = await jwt_util.verify_token(request)  # 用户鉴权
    if not user_id:
        return abort(error_code)

    body = await request.json()
    conversation_id = body.get('conversation_id')
    if not conversation_id:
        return abort(400)

    chats = await MessageModel().get_messages(conversation_id)
    return jsonify(chats)
