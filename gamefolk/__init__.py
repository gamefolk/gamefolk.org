"""Registers modules and initializes the application."""
import http.client
import os

from flask import Flask, send_from_directory
from flask.ext.mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('GAMEFOLK_SETTINGS')

db = SQLAlchemy(app)

from gamefolk.users.models import User, Role
from gamefolk.users.forms import ExtendedRegisterForm
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                    confirm_register_form=ExtendedRegisterForm)

mail = Mail(app)

# Register blueprints. This must be done after the database is created.
from gamefolk.general.views import mod as general_module
from gamefolk.guide.views import mod as guide_module
from gamefolk.shop.views import mod as shop_module
from gamefolk.users.views import mod as users_module
app.register_blueprint(general_module)
app.register_blueprint(guide_module)
app.register_blueprint(shop_module)
app.register_blueprint(users_module)

from gamefolk import assets
assets.init_app(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(http.client.INTERNAL_SERVER_ERROR)
def server_error_handler(error):
    """Cleanup the database and show an error page."""
    db.session.rollback()
    return 'Internal Server Error.', http.client.INTERNAL_SERVER_ERROR

if __name__ == "__main__":
    app.run(debug=True)
