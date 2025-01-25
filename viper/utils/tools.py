import hashlib
import uuid
from datetime import datetime


def generate_uuid():
    random_uuid = uuid.uuid4()
    uuid_str = str(random_uuid)
    md5_hash = hashlib.md5()
    md5_hash.update(uuid_str.encode())
    return md5_hash.hexdigest()  # result is lower


def current_time():
    return datetime.now()
