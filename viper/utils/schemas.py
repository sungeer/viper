from cerberus import Validator

from viper.utils.errors import ValidationError


def validate_data(data, schema):
    validator = Validator()
    is_valid = validator.validate(data, schema)
    if not is_valid:
        raise ValidationError(validator.errors)
    return validator.document


access_token_schema = {
    'phone_number': {
        'type': 'string',
        'minlength': 10,
        'maxlength': 15,
        'regex': '^(?:\\+?\\d{1,3})?\\d{10,15}$',
        'required': True
    },
    'password': {
        'type': 'string',
        'minlength': 6,
        'required': True
    }
}

chat_id_schema = {
    'title': {
        'type': 'string',
        'required': True,  # 必填
        'maxlength': 20,
        'empty': False  # 字符串不能为空
    }
}

send_message_schema = {
    'conversation_id': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'content': {
        'type': 'string',
        'required': True,
        'empty': False
    }
}

get_messages_schema = {
    'conversation_id': {
        'type': 'string',
        'required': True,
        'empty': False
    }
}
