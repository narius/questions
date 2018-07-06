from flask import (
    app,
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    json
)
import logging
import code
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from .database import engine
from .auth import login_required
from flask import current_app
#from flaskr.auth import login_required
from flask import current_app as app
#from flaskr.auth import login_required

bp = Blueprint('questions', __name__)

def get_all_questions():
    app.logger.info('Get all questions')
    db = engine.connect()
    questions = db.execute(
        "SELECT questions.id, questions.text AS text, STRING_AGG(DISTINCT tags.text, ',') AS tags_text, count(DISTINCT votes.id) AS votes FROM questions"
        " INNER JOIN votes ON votes.question_id=questions.id"
        " LEFT JOIN question_tags on question_tags.question_id=questions.id"
        " LEFT JOIN tags on tags.id=question_tags.tag_id"
        " GROUP BY questions.id"
        " ORDER BY count(votes.id) DESC").fetchall()
    # Creates array from tags
    for q in questions:
        d = dict(q.items())
        if d['tags_text']!=None:
            d['tags_text']=d['tags_text'].split(',')
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


# Add tags to question
@bp.route('/add_question_tag', methods=('GET', 'POST'))
def add_question_tag():
    db = engine.connect()
    tag = request.form['tag']
    q_id = int(request.form['q_id'])
    query= "INSERT INTO question_tags(question_id, tag_id) VALUES({}, (SELECT tags.id FROM tags WHERE lower(tags.text)='{}'))".format(q_id,tag.lower())
    status = db.execute(query)
    return json.dumps({'status':'OK'});


@bp.route('/new_question', methods=('GET', 'POST'))
@login_required
def new_question():
    if request.method == 'POST':
        db = engine.connect()
        text = request.form['question']
        db.execute("INSERT INTO questions (text, user_id) VALUES('{}','{}')".format(text,session.get('user_id')))
    questions = get_all_questions()
    return render_template('questions/simple_new.html',title="New Question", text="Question", questions=questions)


@bp.route('/new_tag', methods=('GET', 'POST'))
@login_required
def new_tag():
    if request.method == 'POST':
        db = engine.connect()
        text = request.form['question']
        db.execute("INSERT INTO tags (text) VALUES('{}')".format(text))
    questions = get_all_questions()
    return render_template('questions/simple_new.html',title="New Tag", text="Tag", questions=questions)


@bp.route('/details/<int:question_id>', methods=('GET',))
def details(question_id):
    db = engine.connect()
    votes=db.execute("SELECT TO_CHAR(created_date, 'YYYY-MM-dd') as date, count(votes.id) AS votes from votes where votes.question_id='{}' group by votes.created_date order by date"
    .format(question_id))
    question_data=db.execute("SELECT questions.text AS text, count(votes.id) AS votes"
    " FROM questions"
    " INNER JOIN votes on question_id=questions.id  where questions.id='{}' GROUP BY questions.text".format(question_id))
    row=question_data.fetchone()
    question=row[0]
    q_tags=[]
    all_tags=[]
    unused_tags=[]
    number_of_votes=row[1]
    question_tags=db.execute("SELECT tags.text AS tag_text, question_tags.question_id AS q_id FROM tags"
        " JOIN question_tags ON question_tags.tag_id=tags.id"
        " WHERE question_tags.question_id={}"
        " ORDER BY tags.text".format(question_id))
    all_tags_q=db.execute("SELECT tags.text AS tag_text FROM tags")
    for qt in question_tags:
        q_tags.append(qt['tag_text'])
    for t in all_tags_q:
        all_tags.append(t['tag_text'])
    unused_tags=list(set(all_tags)-set(q_tags))]
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
                           question=question,
                           q_tags=q_tags,
                           q_id=question_id,
                           unused_tags=unused_tags)


# Route for tags
@bp.route('/tags', methods=('GET',))
def tags():
    db = engine.connect()
    tags = db.execute(
    "SELECT tags.id, tags.text AS text, count(questions.id) AS number_of_questions FROM tags"
    " LEFT JOIN question_tags ON tags.id=question_tags.tag_id"
    " LEFT JOIN questions ON question_tags.question_id=questions.id"
    " GROUP BY tags.id"
    " ORDER BY tags.text").fetchall()
    return render_template('questions/tags.html',tags=tags)

# Route for tag details
@bp.route('/details/<string:tag_text>', methods=('GET',))
def tag_details(tag_text):
    db = engine.connect()
    details = db.execute(
    "SELECT tags.id AS tag_id, tags.text AS tag_text, questions.id AS question_id, questions.text AS question_text FROM tags"
    " JOIN question_tags ON question_tags.tag_id=tags.id"
    " JOIN questions ON questions.id=question_tags.question_id"
    " WHERE tags.text='{}'".format(tag_text)).fetchall()
    return render_template('questions/tag_details.html',tag_text=tag_text, details=details)