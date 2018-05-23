from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from database import engine
#from flaskr.auth import login_required

bp = Blueprint('questions', __name__)

@bp.route('/')
def index():
    #db.get_db()
    db = engine.connect()
    questions = db.execute(
        'SELECT questions.id, questions.text AS text, count(votes.id) AS votes from questions'
        ' LEFT JOIN votes ON questions.id=votes.question_id  group by questions.id').fetchall()
    for q in questions:
        print(type(q))
    return render_template('questions/index.html', questions=questions)
