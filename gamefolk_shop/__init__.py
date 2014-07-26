import http.client
import os.path

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('GAMEFOLKSHOP_SETTINGS')

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Register blueprints. This must be done after the database is created.
from gamefolk_shop.general.views import mod as general_module
from gamefolk_shop.users.views import mod as users_module
app.register_blueprint(general_module)
app.register_blueprint(users_module)

from gamefolk_shop.assets import assets
assets.init_app(app)

@app.errorhandler(http.client.INTERNAL_SERVER_ERROR)
def server_error_handler(error):
    """Cleanup the database and show an error page."""
    db.session.rollback()
    return 'Internal Server Error.', http.client.INTERNAL_SERVER_ERROR

if __name__ == "__main__":
    app.run(debug=True)
