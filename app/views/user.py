from flask import request
from flask_restx import Resource, Namespace, abort

from app.dao.model.user import UserSchema
from app.implemented import user_service


user_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        return users_schema.dump(user_service.get_all()), 200


@user_ns.route('/<int:bid>')
class UsersView(Resource):
    def get(self, bid):
        return user_schema.dump(user_service.get_one(bid)), 200


    def patch(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204


@user_ns.route('/password/<int:bid>')
class UseresView(Resource):
    def put(self, bid):
        req_json = request.json
        if None in [req_json.get("password_1"), req_json.get("password_2")]:
            abort(400)
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204