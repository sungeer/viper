"""
命令行下的酷炫显示
"""
import httpx
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

console = Console(width=100)


def fetch_stream(access_token, content, conversation_id):
    url = 'http://bebinca.cc/chat/send-message'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'content': content,
        'conversation_id': conversation_id
    }
    s = []
    with httpx.Client() as client:
        with client.stream('POST', url, json=data, headers=headers) as response:
            for line in response.iter_raw():
                ret = line.decode('utf-8')
                if ret.endswith('\n'):
                    ret = ret[:-1]
                s.append(ret)
                yield ret


def run(access_token, content, conversation_id):
    output_buffer = ''
    with Live(console=console, refresh_per_second=4) as live:
        for chunk in fetch_stream(access_token, content, conversation_id):
            output_buffer += chunk
            md = Markdown(output_buffer)
            live.update(md)


if __name__ == '__main__':
    access_token = 'eyJhbGciOfAN3njep8'
    conversation_id = '113afde1d3c782b20'
    content = '帮我写个斐波那契函数'
    run(access_token, content, conversation_id)
