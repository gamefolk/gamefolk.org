import random
import string

from flask.ext.security import UserMixin, RoleMixin, user_registered

from gamefolk import db


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    """A user of the shop."""
    id = db.Column(db.Integer, primary_key=True)        # pylint: disable=C0103
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    secret_code = db.Column(db.String(20))

    def __repr__(self):
        return '<User %r>' % self.id


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


def create_secret_code():
    """Generates a 6 character alphanumeric code to be used to verify that
    the user has purchased a cartridge."""
    characters = string.ascii_uppercase + string.digits
    size = 6
    return ''.join(random.choice(characters) for _ in range(size))
