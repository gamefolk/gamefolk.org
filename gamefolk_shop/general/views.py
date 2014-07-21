from flask import Blueprint, render_template

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
    return render_template('general/index.html')
