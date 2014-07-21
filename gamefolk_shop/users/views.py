from flask import (Blueprint, request, render_template, flash, g, session,
    redirect, url_for, current_app)
from flask.ext.login import (login_required, current_user, login_user,
    logout_user)

from gamefolk_shop import db, login_manager
from gamefolk_shop.users.forms import LoginForm, RegisterForm
from gamefolk_shop.users.models import User

mod = Blueprint('users', __name__, url_prefix='/users')

login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@mod.route('/me')
@login_required
def profile():
    return render_template("users/profile.html", user=current_user)

@mod.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Thanks for registering!")
        return redirect(url_for('users.profile'))
    return render_template('users/register.html', form=form)

@mod.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Successfully logged in as %s.' % user.name)
            return redirect(request.args.get('next') or
                url_for('users.profile'))
        flash('Incorrect email or password.', 'error-message')
    return render_template("users/login.html", form=form)

@mod.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('general.index'))
