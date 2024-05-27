from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii


class MyCipher:
    def __init__(self, key):
        self.key = key
        if len(self.key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes long")

    def aes_encryption(self, txt):
        nonce = get_random_bytes(16)  # Generate a new nonce for each encryption
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(txt.encode('utf-8'))
        return binascii.hexlify(nonce).decode('utf-8'), binascii.hexlify(ciphertext).decode('utf-8'), binascii.hexlify(
            tag).decode('utf-8')

    def aes_decryption(self, nonce_hex, ciphertext_hex, tag_hex):
        nonce = binascii.unhexlify(nonce_hex)
        ciphertext = binascii.unhexlify(ciphertext_hex)
        tag = binascii.unhexlify(tag_hex)

        try:
            cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode('utf-8')
        except (ValueError, KeyError) as e:
            print("Decryption failed:", str(e))
            return None
