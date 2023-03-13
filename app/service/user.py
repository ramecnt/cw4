import base64
import hashlib
import hmac

from app.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

from app.dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def create(self, user_d):
        user_d['password'] = self.generate_password(user_d['password'])
        return self.dao.create(user_d)

    def update(self, user_d):
        user = self.dao.get_one(user_d["id"])
        if "password_1" in user_d:
            if self.generate_password(user_d["password_1"]) == user.password:
                user_d["password"] = self.generate_password(user_d.get('password_2'))
            else:
                raise Exception
        self.dao.update(user_d)
        return self.dao

    def delete(self, bid):
        self.dao.delete(bid)

    def get_by_email(self, username):
        return self.dao.get_by_email(username)

    def generate_password(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )).decode('utf-8')

    def compare_password(self, password_hash, password_other):
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac(
                'sha256',
                password_other.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            ))
