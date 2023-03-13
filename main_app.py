from flask import Flask, render_template
from flask_restx import Api
from flask_cors import CORS

from app.config import Config
from app.setup_db import db
from app.views.auth import auth_ns
from app.views.directors import director_ns
from app.views.genres import genre_ns
from app.views.movies import movie_ns
from app.views.user import user_ns

api = Api(doc="/docs")


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api.init_app(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()
        #
        # u1 = User(e_mail="n.ilin@it-park.tech", password="my_little_pony", name="kolya", surname="ilin",
        #           favorite_genre="thriller")
        # u2 = User(e_mail="e.arhipov@it-park.tech", password="qwerty", name="egor", surname="arhipov",
        #           favorite_genre="comedy")
        # u3 = User(e_mail="r.boronov@it-park.tech", password="P@ssw0rd", name="roma", surname="boronov",
        #           favorite_genre="retro")

        # with db.session.begin():
        #     db.session.add_all([u1, u2, u3])


config = Config()
app = create_app(config)
app.debug = True
CORS(app)


if __name__ == '__main__':
    app.run()
