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
import code
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from .database import engine
from .auth import login_required
#from flaskr.auth import login_required

bp = Blueprint('questions', __name__)

def get_all_questions():
    db = engine.connect()
    questions = db.execute(
        'SELECT questions.id as id, questions.text AS text, count(votes.id) AS votes from questions'
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
    return render_template('questions/simple_new.html',title="New Question", text="Question", questions=questions)

@bp.route('/details/<int:question_id>', methods=('GET',))
def details(question_id):
    db = engine.connect()
    votes=db.execute("SELECT TO_CHAR(created_date, 'YYYY-MM-dd') as date, count(votes.id) AS votes from votes where votes.question_id='{}' group by votes.created_date order by date"
    .format(question_id))
    question_data=db.execute("SELECT questions.text AS text, count(votes.id) AS votes FROM questions INNER JOIN votes on question_id=questions.id  where questions.id='{}' GROUP BY questions.text".format(question_id))
    row=question_data.fetchone()
    question=row[0]
    number_of_votes=row[1]
    #["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    labels = ''
    data = ''
    for v in votes:
        labels = labels+'\"'+str(v['date'])+'\",'
        data = data+str(v['votes'])+','
    labels = '['+labels[:-1]+']'
    data = '['+data[:-1]+']'
    
    #code.interact(local=locals())
    print(votes)
    return render_template('questions/details.html',
                           labels=labels,
                           data=data,
                           number_of_votes=number_of_votes,
                           question=question)
