from flask import render_template, request, redirect, url_for, flash, session, g, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select, update, delete
from api.database import db_session
from api.models import User
from api.auth import auth
from api.auth.decorators import login_required


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
        except KeyError as e:
            flash(f"Missing field: {e.args[0]}", 'error')
            return render_template('register.html')

        if not username or not password or not role:
            flash("Username, password, and role are required.", 'error')
            return render_template('register.html')

        # Check if user already exists
        stmt = select(User).where(User.username == username)
        existing_user = db_session.execute(stmt).scalar()

        if existing_user:
            flash(
                "User already registered. Please specify a different username.", 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db_session.add(new_user)
        db_session.commit()
        flash("Successfully registered.", 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        stmt = select(User).where(User.username == username)
        user = db_session.execute(stmt).scalar()

        if user and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            flash("Successfully logged in.", 'success')
            # Replace 'index' with your endpoint
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", 'error')

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out.", 'success')
    return redirect(url_for('auth.login'))


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        stmt = select(User).where(User.id == user_id)
        g.user = db_session.execute(stmt).scalar()


@auth.after_app_request
def log_session_data(response):
    current_app.logger.debug(
        f"Active User: {session.get('user_id')}")
    current_app.logger.debug(
        f"Session Modified?: {session.modified}")
    return response


@auth.get('/users')
@login_required
def get_users():
    stmt = select(User)
    users = db_session.execute(stmt).scalars().all()
    return render_template('users/list.html', users=users)


@auth.get('/users/<int:id>')
@login_required
def user_detail(id: int):
    stmt = select(User).where(User.id == id)
    user = db_session.execute(stmt).scalar()
    if user is None:
        flash('User not found.', 'error')
        return redirect(url_for('auth.get_users'))
    return render_template('users/detail.html', user=user)


@auth.post('/users/<int:id>')
@login_required
def update_user(id: int):
    if request.method == 'POST':
        # Assuming data is sent via form
        data = request.form
        stmt = update(User).where(User.id == id).values(**data)
        db_session.execute(stmt)
        db_session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('auth.user_detail', id=id))
    # For GET request or initial load
    stmt = select(User).where(User.id == id)
    user = db_session.execute(stmt).scalar()
    return render_template('users/update.html', user=user)


@auth.delete('/users/<int:id>')
@login_required
def delete_user(id: int):
    stmt = delete(User).where(User.id == id)
    result = db_session.execute(stmt)
    db_session.commit()
    if result.rowcount == 0:
        flash('User not found.', 'error')
    else:
        flash('User deleted successfully.', 'success')
    return redirect(url_for('auth.get_users'))
