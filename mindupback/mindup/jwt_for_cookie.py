import jwt


secret_key = 'my_secret_key064387632'


def encode(payload: dict):
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode(token: str):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms='HS256')
        return decoded_token
    except jwt.InvalidTokenError:
        return None
