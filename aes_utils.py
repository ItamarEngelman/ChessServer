# from diffiehellman import DiffieHellman
# class Cipher:
#     @staticmethod
#     def get_dh_public_key(self):
#         dh = DiffieHellman(group=14, key_bits=540)
#         pk = dh.get_public_key()
#         return dh, pk
#     @staticmethod
#     def get_dh_shared_key(dh_1, pk_2, lngth=32):
#         dh_shared = dh_1.generate_shared_key(pk_2)
#         return dh_shared[:lngth]
#
#     @staticmethod
#     def print_dh(dh, peer_pk, role):
#         shared_key = Cipher.get_dh_shared_key(dh, peer_pk)
#         print(role)
#         print("prime : ", dh._prime, "\nprivate key:", dh.get_public_key(), "\n shared key", shared_key)



# from Crypto.Cipher import AES
# from cryptography.hazmat.primitives.ciphers import Cipher as CryptographyCipher, algorithms, modes
#
# class MyCipher:
#     def __init__(self, key, nonce):
#         self.key = key
#         self.nonce = nonce
#
#     def aes_encryption(self, txt):
#         cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)
#         ciphertext, tag = cipher.encrypt_and_digest(txt.encode('utf-8'))
#         return ciphertext, tag
#
#     def aes_decryption(self, ciphertext, tag):
#         cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)
#         plaintext = cipher.decrypt_and_verify(ciphertext, tag)
#         return plaintext.decode('utf-8')
#
# # Example usage
# key = b'Sixteen byte key'
# nonce = b'UniqueNonce123'  # Ensure the nonce is 16 bytes for AES
#
# cipher = MyCipher(key, nonce)
#
# # Encrypt
# plaintext = 'Hello, World!'
# ciphertext, tag = cipher.aes_encryption(plaintext)
# print(f'Ciphertext: {ciphertext}')
#
# # Decrypt
# decrypted_text = cipher.aes_decryption(ciphertext, tag)
# print(f'Decrypted text: {decrypted_text}')


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

class SimpleAES:
    def __init__(self, key):
        self.key = key
        self.backend = default_backend()
        self.block_size = algorithms.AES.block_size

    def encrypt(self, plaintext):
        iv = os.urandom(self.block_size)  # Use block size for IV
        print("IV:", iv)  # Add this line to print the IV
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data

    def decrypt(self, ciphertext):
        iv = ciphertext[:self.block_size]  # Extract IV from ciphertext
        print("IV:", iv)  # Add this line to print the IV
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(ciphertext[self.block_size:]) + decryptor.finalize()
        unpadder = padding.PKCS7(self.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode()
