from cerberus import Validator

from viper.utils.errors import ValidationError


def validate_data(data, schema):
    validator = Validator()
    is_valid = validator.validate(data, schema)
    if not is_valid:
        raise ValidationError(validator.errors)
    return validator.document
