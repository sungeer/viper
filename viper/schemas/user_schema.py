access_token_schema = {
    'type': 'object',
    'properties': {
        'phone': {
            'type': 'string',
            'pattern': r'^1[3-9]\d{9}$'  # 中国大陆手机号码正则
        },
        'password': {
            'type': 'string',
            'minLength': 6,  # 密码最小长度
            'maxLength': 12  # 密码最大长度
        }
    },
    'required': ['phone', 'password']  # 必填字段
}
