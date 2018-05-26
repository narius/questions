import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from auth import bp as bp_auth
from questions import bp as bp_questions

from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
toolbar = DebugToolbarExtension(app)
#db = SQLAlchemy(app)

app.register_blueprint(bp_questions, url_prefix='/')
app.register_blueprint(bp_auth, url_prefix='/auth')
#from models import User

if __name__ == '__main__':
    app.run()
