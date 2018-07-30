import json


def decode_qrcode(qr_data):
    return json.loads(qr_data)
