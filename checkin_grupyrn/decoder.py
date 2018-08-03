import json
from cryptography.fernet import Fernet
from checkin_grupyrn import config


def decode_qrcode(qr_data):
    cipher_suite = Fernet(str(config.get('crypto_key')))
    decrypted_data = cipher_suite.decrypt(str(qr_data))
    return json.loads(decrypted_data)