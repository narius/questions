import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from questions import bp
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
toolbar = DebugToolbarExtension(app)
#db = SQLAlchemy(app)

app.register_blueprint(bp, url_prefix='/')
#from models import User

if __name__ == '__main__':
    app.run()
