"""Routes related to the Gamefolk guide to Gameboy programming."""
from flask import Blueprint, render_template
from flask.ext.markdown import Markdown

from gamefolk import app

Markdown(app, extensions=['fenced_code'])

mod = Blueprint('guide', __name__, url_prefix='/guide')


@mod.route('/')
def guide():
    """Shows all of the content contained in the guide."""
    return render_template('guide/guide.html')
