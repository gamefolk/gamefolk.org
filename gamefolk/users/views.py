"""User-related views."""

from flask import (Blueprint, request, render_template, flash, redirect, \
    url_for)
from flask.ext.login import (login_required, current_user, login_user, \
    logout_user)

from gamefolk import db, login_manager
from gamefolk.users.forms import LoginForm, RegisterForm
from gamefolk.users.models import User

mod = Blueprint('users', __name__, url_prefix='/users')

login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    """Retrieve a user object from the database."""
    return User.query.filter_by(id=user_id).first()

@mod.route('/me')
@login_required
def profile():
    """The current user's profile page."""
    return render_template("users/profile.html", user=current_user)

@mod.route('/register', methods=['GET', 'POST'])
def register():
    """New registration page."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Thanks for registering!", 'info')
        return redirect(url_for('users.profile'))
    return render_template('users/register.html', form=form)

@mod.route('/login', methods=['GET', 'POST'])
def login():
    """On a GET request, returns the login page. On a POST request, validates
    the user's credentials and logs them in if they are correct."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Successfully logged in.', 'success')
            return redirect(request.args.get('next') or \
                url_for('users.profile'))
        flash('Incorrect email or password.', 'alert')
    return render_template("users/login.html", form=form)

@mod.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('general.index'))
