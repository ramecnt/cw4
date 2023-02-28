from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.user import UserSchema
from app.implemented import user_service
from app.decorators import admin_required, auth_required

user_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UsersViews(Resource):
    @admin_required
    def get(self):
        return users_schema.dump(user_service.get_all()), 200

    def post(self):
        req_json = request.json
        user_service.create(req_json)
        return '', 201


@user_ns.route('/<int:bid>')
class UsersView(Resource):
    @admin_required
    def get(self, bid):
        return user_schema.dump(user_service.get_one(bid)), 200
    @auth_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204

    @auth_required
    def delete(self, bid):
        user_service.delete(bid)
        return '', 204
