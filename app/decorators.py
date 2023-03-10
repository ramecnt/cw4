import jwt
from flask import request, abort

from app.constants import PWD_SECRET, PWD_ALGORITHM


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        try:
            jwt.decode(token, PWD_SECRET, algorithms=[PWD_ALGORITHM])
        except Exception as e:
            print(f"Traceback: {e}")
            abort(401)

        return func(*args, **kwargs)

    return wrapper



