import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .auth import bp as bp_auth
from .questions import bp as bp_questions
from .config import *
from flask_debugtoolbar import DebugToolbarExtension
import logging
from logging.handlers import RotatingFileHandler
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config.from_object('config.DevelopmentConfig')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['REGISTRATION_KEY']=os.environ['REGISTRATION_KEY']
    
    db = SQLAlchemy(app)
    toolbar = DebugToolbarExtension(app)
    #db = SQLAlchemy(app)
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('foo.log', maxBytes=10000000, backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.register_blueprint(bp_questions, url_prefix='/')
    app.register_blueprint(bp_auth, url_prefix='/auth')
    #from models import User
    app.log=logging.getLogger('flask.app')
    return app
#if __name__ == '__main__':
#    app.run()
