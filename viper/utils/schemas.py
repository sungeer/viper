from dataclasses import dataclass
from datetime import datetime

from cerberus import Validator

from viper.utils.errors import ValidationError


@dataclass
class UserSchema:
    id: int
    name: str
    phone: str
    created_time: datetime
    is_admin: bool = False


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
