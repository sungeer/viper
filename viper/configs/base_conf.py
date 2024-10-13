from pathlib import Path


class BaseSettings:
    app_name = 'viper'

    # Path(__file__).resolve() 获取 当前文件 的 绝对路径
    # parents 属性是一个包含 父目录 的 序列
    # parents[2] 返回上 三层目录
    basedir = Path(__file__).resolve().parents[2]

    jwt_algorithm = 'HS256'  # 加密算法
    access_token_expire_minutes = 1440  # token 有效期 1440 即 24h

    ai_url = 'https://ai-api.betteryeah.com'
