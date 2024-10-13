from base64 import b64encode, b64decode

from Crypto.Cipher import AES  # pip install pycryptodome
from Crypto.Util.Padding import pad, unpad

from viper.configs import settings


class AESCipher:

    def __init__(self, key):
        key_hex = key  # type(key) is string
        key_bytes = bytes.fromhex(key_hex)  # bytes
        if len(key_bytes) not in (16, 24, 32):
            raise ValueError('sec_key is error')
        self.key = key_bytes

    def encrypt(self, data):  # 加密
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        ct = b64encode(ct_bytes).decode('utf-8')
        return ct

    def decrypt(self, data):  # 解密
        ct = b64decode(data)
        cipher = AES.new(self.key, AES.MODE_ECB)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')


key = settings.sec_key
cipher = AESCipher(key)

if __name__ == '__main__':
    import secrets

    key_hex = secrets.token_hex(16)  # 生成十六进制字符串
    key_bytes = bytes.fromhex(key_hex)  # 转换为字节字符串
    print(key_hex)

    passwd = 'zaq1xsw2cde'
    encrypted = cipher.encrypt(passwd)  # 加密
    print(encrypted)

    decrypted = cipher.decrypt(encrypted)  # 解密
    print(decrypted)
