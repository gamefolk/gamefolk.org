"""Routes that don't fit a particular module."""
from flask import Blueprint, render_template

mod = Blueprint('general', __name__)


@mod.route('/')
def index():
    """Application landing page."""
    return render_template('general/index.html')
