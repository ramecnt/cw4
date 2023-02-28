from flask import Flask
from flask_restx import Api

from app.config import Config
from app.dao.model.user import User
from app.setup_db import db
from app.views.auth import auth_ns
from app.views.directors import director_ns
from app.views.genres import genre_ns
from app.views.movies import movie_ns
from app.views.user import user_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.create_all()

        u1 = User(username="vasya", password="my_little_pony", role="user")
        u2 = User(username="oleg", password="qwerty", role="user")
        u3 = User(username="oleg", password="P@ssw0rd", role="admin")

        with db.session.begin():
            db.session.add_all([u1, u2, u3])


config = Config()
app = create_app(config)
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
