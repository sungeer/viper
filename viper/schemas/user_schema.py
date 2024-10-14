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
