from binascii import b2a_hex
from Crypto.Util.Padding import pad

from Crypto.Cipher import AES  # pip install pycryptodomex


def encrypt_data(plaintext, seckey):
    if len(seckey) not in [16, 24, 32]:
        raise ValueError(f'The length of the seckey must be 16, 24, or 32, it cannot be {len(seckey)}.')

    plaintext_padded = pad(plaintext.encode(), AES.block_size)
    aes = AES.new(seckey.encode(), AES.MODE_ECB)
    encrypted_data = aes.encrypt(plaintext_padded)
    return b2a_hex(encrypted_data).decode()


if __name__ == '__main__':
    pass
