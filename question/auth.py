import functools

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
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from database import engine
#from flaskr.auth import login_required

bp = Blueprint('auth', __name__)
db = engine.connect()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    db = engine.connect()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            "SELECT id FROM users WHERE username = '{}'".format(username)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                "INSERT INTO users (username, password) VALUES ('{}', '{}')".format(username, generate_password_hash(password))
            )
            #engine.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE username = '{}'".format(username)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('questions.index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None

    else:
        g.user = db.execute(
            "SELECT * FROM users WHERE id = '{}'".format(user_id)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('questions.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
