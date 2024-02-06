# secure_login.py
from cryptography.fernet import Fernet
import os

def load_or_generate_key():
    key_path = 'encryption.key'
    if os.path.exists(key_path):
        with open(key_path, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
        return key

def encrypt_message(message, key):
    return Fernet(key).encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    return Fernet(key).decrypt(encrypted_message).decode()

def save_login_details(user_id, password):
    key = load_or_generate_key()
    encrypted_user_id = encrypt_message(user_id, key)
    encrypted_password = encrypt_message(password, key)
    with open('secure_login', 'wb') as file:
        file.write(encrypted_user_id + b'\n' + encrypted_password)

def load_login_details():
    key = load_or_generate_key()
    if os.path.exists('secure_login'):
        with open('secure_login', 'rb') as file:
            encrypted_user_id, encrypted_password = file.read().split(b'\n')
            user_id = decrypt_message(encrypted_user_id, key)
            password = decrypt_message(encrypted_password, key)
            return user_id, password
    return None, None
