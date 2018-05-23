import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from questions import bp

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

app.register_blueprint(bp, url_prefix='/q')
#from models import User

@app.route('/')
def hello():
    print(os.environ['APP_SETTINGS'])
    return "Hello World!"

if __name__ == '__main__':
    app.run()
