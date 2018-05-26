from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from database import engine
from auth import login_required
#from flaskr.auth import login_required

bp = Blueprint('questions', __name__)

def get_all_questions():
    db = engine.connect()
    questions = db.execute(
        'SELECT questions.id, questions.text AS text, count(votes.id) AS votes from questions'
        ' LEFT JOIN votes ON questions.id=votes.question_id  group by questions.id order by votes desc').fetchall()
    return questions

def vote(question_id):
    db = engine.connect()
    query= 'INSERT INTO votes (question_id) VALUES({})'.format(question_id)
    status = db.execute(query)
    return status

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        vote(request.form['vote'])
    questions = get_all_questions()
    return render_template('questions/index.html', questions=questions)

@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new():
    if request.method == 'POST':
        db = engine.connect()
        text = request.form['question']
        db.execute("INSERT INTO questions (text, user_id) VALUES('{}','{}')".format(text,session.get('user_id')))
    questions = get_all_questions()
    return render_template('questions/new_question.html', questions=questions)
