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


def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        token = request.headers["Authorization"].split("Bearer ")[-1]
        role = None
        try:
            user_token = jwt.decode(token, PWD_SECRET, algorithms=[PWD_ALGORITHM])
            role = user_token.get("role", "user")
            print(role)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper
