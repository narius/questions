import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select, func
from .auth import bp as bp_auth
from .questions import bp as bp_questions
from .config import *
from flask_debugtoolbar import DebugToolbarExtension
import logging
from flask_migrate import Migrate
from datetime import datetime
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()

#def create_app():
#    app = Flask(__name__)
#    
#    return app
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config.from_object('config.DevelopmentConfig')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['REGISTRATION_KEY']=os.environ['REGISTRATION_KEY']
    
    db.init_app(app)
    migrate = Migrate(app, db)
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
if __name__ == '__main__':
    app.run()


question_tags = db.Table('question_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True)
)
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    questions = db.relationship('Question', backref='user', lazy=True)
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    votes = db.relationship('Vote', backref='question', lazy=True)
    tags = db.relationship('question_tags', secondary=question_tags, lazy='subquery',
        backref=db.backref('questions', lazy=True))
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False,
        server_default=db.func.now())
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    def __init__(self):
        pass

    def __repr__(self):
        return '<id {}, question {}'.format(self.id, self.question_id)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    questions = db.relationship('question_tags', secondary=question_tags, lazy='subquery',
        backref=db.backref('tags', lazy=True))
    def __init__(self,text):
        self.text=text

    def __repr__(self):
        return '<id {}>'.format(self.id)


