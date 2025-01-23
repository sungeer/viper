from pathlib import Path

from starlette.config import Config

CURRENT_DIR = Path(__file__).resolve()  # 当前文件 的 绝对路径
BASE_DIR = CURRENT_DIR.parent.parent.parent

CONF = Config('.env')
