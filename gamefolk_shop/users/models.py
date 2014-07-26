from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from gamefolk_shop import db

class User(UserMixin, db.Model):
    """A user of the shop."""
    id = db.Column(db.Integer, primary_key=True)        # pylint: disable=C0103
    email = db.Column(db.String(120), unique=True)
    _password_hash = db.Column(db.String(160))

    def __init__(self, password, email):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Automatically hash and salt the given password, then store it in the
        database."""
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the given password matches the hashed and salted password
        stored in the database."""
        return check_password_hash(self._password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.id
