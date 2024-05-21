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



#from Crypto.Cipher import AES
#class Cipher:
#    def __init__(self, key, nonce):
#        self.key = key
#        self.nonce = nonce
#    def aes_encryption(self, txt):
#        cipher = AES.new(self.key, AES.MODE_EAX, nonce = self.nonce)
#        ciphertext, tag = cipher.
