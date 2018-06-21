import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .auth import bp as bp_auth
from .questions import bp as bp_questions
from .config import *
from flask_debugtoolbar import DebugToolbarExtension

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config.from_object('config.DevelopmentConfig')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db = SQLAlchemy(app)
    toolbar = DebugToolbarExtension(app)
    #db = SQLAlchemy(app)

    app.register_blueprint(bp_questions, url_prefix='/')
    app.register_blueprint(bp_auth, url_prefix='/auth')
    #from models import User
    return app
#if __name__ == '__main__':
#    app.run()
