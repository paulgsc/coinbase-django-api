from cryptography.fernet import Fernet
from django.conf import settings


class CryptoUtils:
    @staticmethod
    def generate_encryption_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_data(data, encryption_key):
        cipher_suite = Fernet(encryption_key)
        encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
        return encrypted_data

    @staticmethod
    def decrypt_data(encrypted_data, encryption_key):
        cipher_suite = Fernet(encryption_key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
        return decrypted_data