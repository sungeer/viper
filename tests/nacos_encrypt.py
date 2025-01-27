from binascii import b2a_hex
from Crypto.Util.Padding import pad

from Crypto.Cipher import AES  # pip install pycryptodomex


def encrypt_sec(plaintext, seckey):
    if len(seckey) not in [16, 32]:
        raise ValueError(f'The length of the seckey must be 16, or 32, it cannot be {len(seckey)}.')
    plaintext_padded = pad(plaintext.encode(), AES.block_size)
    aes = AES.new(seckey.encode(), AES.MODE_ECB)
    encrypted_data = aes.encrypt(plaintext_padded)
    return b2a_hex(encrypted_data).decode()


if __name__ == '__main__':
    pt = 'admin'
    sk = '1f2095a2ec0cefd2c2ab9dd258ad22c3'
    es = encrypt_sec(pt, sk)
    print(es)
