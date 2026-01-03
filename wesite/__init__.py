from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

DB_NAME = "miniblog.db"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "nothing"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # blueprints
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    # import models (IMPORTANT)
    from .models import UserInfo,Blog, BlogComment, BlogReaction

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return UserInfo.query.get(int(id))

    return app


def create_database(app):
    db_path = path.join(app.root_path, DB_NAME)

    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
        print("✅ Database created!")
