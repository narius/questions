from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

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
    # addresses = db.relationship('Address', backref='person', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    votes = db.relationship('Vote', backref='question', lazy=True)
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    def __init__(self):
        pass

    def __repr__(self):
        return '<id {}, question {}'.format(self.id, self.question_id)
