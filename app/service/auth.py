import datetime
import calendar
import jwt

from app.constants import PWD_SECRET, PWD_ALGORITHM
from app.service.user import UserService


class AuthService:
    def __init__(self, service: UserService):
        self.service = service

    def generate_token(self, e_mail, password, refresh=False):
        user = self.service.get_by_email(e_mail)

        if user is None:
            raise Exception()

        if not refresh:
            if not self.service.compare_password(user.password, password):
                raise Exception()

        data = {
            'e_mail': user.e_mail,
            'password': user.password
        }

        exp_access_token = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(exp_access_token.timetuple())
        access_token = jwt.encode(data, PWD_SECRET, algorithm=PWD_ALGORITHM)

        exp_refresh_token = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(exp_refresh_token.timetuple())
        refresh_token = jwt.encode(data, PWD_SECRET, algorithm=PWD_ALGORITHM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def check_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, PWD_SECRET, algorithms=[PWD_ALGORITHM])
        e_mail = data.get('e_mail')

        user = self.service.get_by_email(e_mail)

        if user is None:
            raise Exception()

        return self.generate_token(user.e_mail, user.password, refresh=True)

