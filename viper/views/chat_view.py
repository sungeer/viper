import json

import httpx
from starlette.responses import StreamingResponse

from viper.configs import settings
from viper.utils import tools
from viper.utils.http_client import httpx_common, httpx_stream
from viper.utils.tools import jsonify, abort
from viper.utils.log_util import logger
from viper.utils.decorators import auth_required, validate_request
from viper.models.chat_model import ChatModel
from viper.models.message_model import MessageModel
from viper.models.content_model import ContentModel
from viper.utils.schemas import chat_id_schema, send_message_schema, get_messages_schema

headers = {
    'Content-Type': 'application/json',
    'Access-key': settings.ai_api_key,
    'Workspace-Id': settings.ai_workspace_id
}


@auth_required
@validate_request(chat_id_schema)
async def get_chat_id(request):
    body = await request.json()
    title = body.get('title')

    url = f'{settings.ai_url}/v1/oapi/agent/chat/conversation/create'
    data = {
        'robot_id': settings.ai_robot_id,
        'user': 'wangxun',
        'title': title
    }
    response = await httpx_common.post(url, headers=headers, json=data)
    response = response.json()
    data = response.get('data')
    conversation_id = data.get('conversation_id')

    user = request.state.user
    user_id = user.id
    await ChatModel().add_chat(conversation_id, title, user_id)
    return jsonify(conversation_id)


async def get_response(conversation_id, content):
    url = f'{settings.ai_url}/v1/oapi/agent/chat'
    data = {
        'robot_id': settings.ai_robot_id,
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


@auth_required
@validate_request(send_message_schema)
async def send_message(request):
    body = await request.json()
    conversation_id = body.get('conversation_id')
    content = body.get('content')

    trace_id = tools.generate_uuid()
    chat_info = await ChatModel().get_chat_by_conversation(conversation_id)
    chat_id = chat_info['ID']

    message_id = await MessageModel().add_message(chat_id, trace_id, 'user')
    await ContentModel().add_content(message_id, content)

    return StreamingResponse(stream_data(conversation_id, chat_id, trace_id, content), media_type='text/event-stream')


# 所有会话
@auth_required
async def get_chats(request):
    user = request.state.user
    user_id = user.id
    chats = await ChatModel().get_chats(user_id)
    return jsonify(chats)


# 所有问答
@auth_required
@validate_request(get_messages_schema)
async def get_messages(request):
    body = await request.json()
    conversation_id = body.get('conversation_id')

    chats = await MessageModel().get_messages(conversation_id)
    return jsonify(chats)
