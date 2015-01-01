"""User-related views."""

from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.security import login_required, current_user, logout_user

mod = Blueprint('users', __name__, url_prefix='/users')


@mod.route('/me')
@login_required
def profile():
    """The current user's profile page."""
    return render_template("users/profile.html", user=current_user)
