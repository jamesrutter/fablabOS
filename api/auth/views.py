from flask import render_template, redirect, url_for, flash, session, g, request
from werkzeug.security import check_password_hash
from sqlalchemy import select
from api.database import db_session
from api.models import User
from api.auth import auth
from api.auth.decorators import login_required, admin_required
from api.auth.controllers import get_users, get_user, delete_user, create_user


# AUTHENTICATION #

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user, error = create_user(request)
        if error:
            flash(error, 'error')
            return render_template('auth/register.html')

        flash("Successfully registered! Please log in.", 'success')
        return redirect(url_for('index'))

    return render_template('auth/register.html')


@auth.post('/login')
def login():
    username = request.form['username']
    password = request.form['password']

    stmt = select(User).where(User.username == username)
    user = db_session.execute(stmt).scalar()

    if user and check_password_hash(user.password, password):
        session.clear()
        session['user_id'] = user.id
        flash(message='Successfully logged in.',category='success')
    else:
        flash(message='Invalid username or password.',category='warning')
    return redirect(url_for('index'))


@auth.post('/logout')
def logout():
    session.clear()
    flash("Successfully logged out.", 'success')
    return redirect(url_for('index'))


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        stmt = select(User).where(User.id == user_id)
        g.user = db_session.execute(stmt).scalar()


# USER MANAGEMENT #

@auth.get('/users')
@login_required
def index():
    users = get_users()
    return render_template('users/index.html', users=users)


@auth.get('/users/<int:id>')
@login_required
def detail(id):
    u = get_user(id)
    return render_template('users/detail.html', u=u)


@auth.route('/users/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        user, error = create_user(request)
        if error:
            flash(error, 'error')
            return render_template('users/create.html')

        flash("User created successfully.", 'success')
        return redirect(url_for('auth.index'))

    return render_template('users/create.html')


@auth.route('/users/<int:id>', methods=['GET', 'PUT'])
@login_required
def update(id: int, ):
    if request.method == 'PUT':
        user, error = create_user(request)
        if error:
            flash(error, 'error')
            return render_template('users/create.html')

        flash("User created successfully.", 'success')
        return redirect(url_for('user_management.index'))

    return render_template('users/create.html')


@auth.delete('/users/<int:id>')
@login_required
def delete(id: int):
    delete_user(id)
    flash('User deleted successfully!')
    return redirect(url_for('auth.index'))


# # ERROR HANDLERS #

# @auth.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404


# @auth.errorhandler(401)
# def unauthorized_access(error):
#     return render_template('401.html'), 401
