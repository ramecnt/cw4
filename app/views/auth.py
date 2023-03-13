from flask import request, abort
from flask_restx import Resource, Namespace

from app.implemented import auth_service
from app.implemented import user_service
from app.decorators import auth_required

auth_ns = Namespace('auth')


@auth_ns.route("/register/")
class AuthsView(Resource):
    def post(self):
        req_json = request.json
        if None in req_json:
            abort(400, "не корректный запрос")
        user_service.create(req_json)
        return "", 200


@auth_ns.route('/login/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email')
        password = req_json.get('password')

        if None in [email, password]:
            abort(401)

        tokens = auth_service.generate_token(email, password)

        return tokens, 201

    @auth_required
    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")

        if refresh_token is None:
            abort(401)

        tokens = auth_service.check_refresh_token(refresh_token)

        return tokens, 201
