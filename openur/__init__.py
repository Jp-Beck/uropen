# This is the entry point for the OpenUR package website.
# It is a Flask application.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from openur.config import Config






# create the extension
db = SQLAlchemy()
# create the app

# create the bcrypt instance
bcrypt = Bcrypt()
# create the login manager instance
login_manager = LoginManager()
# set the login view
login_manager.login_view = 'users.login'


# initialize the mail instance
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize the app with the extension
    db.init_app(app)
    # initialize the bcrypt instance
    bcrypt.init_app(app)
    # initialize the login manager instance
    login_manager.init_app(app)
    # initialize the mail instance
    mail.init_app(app)


    # import the routes
    from openur.main.routes import main
    from openur.users.routes import users
    from openur.posts.routes import posts
    from openur.errors.handlers import errors
    # register the blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
