import jwt
from django.conf import settings


def encode_token(data: str):
    return jwt.encode(data, settings.SECRET_KEY, algorithm='HS256')


def decode_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
