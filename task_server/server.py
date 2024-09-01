from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "task_server_database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '008ccaae-ab00-4abe-a637-e5548f16555e'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from routers.webadmin import webadmin
    from routers.client import client
    # from .auth import auth

    app.register_blueprint(webadmin)
    app.register_blueprint(client)

    # from .models import User

    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print('Created Database!')

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

    return app
