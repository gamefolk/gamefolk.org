from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo

from gamefolk_shop.users.models import User

class LoginForm(Form):
    """Form to log in to the shop."""
    email = TextField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required()])

class RegisterForm(Form):
    """Form to register an account for the shop."""
    name = TextField('Name', [Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('password', message='Passwords must match'),
        ])
    recaptcha = RecaptchaField()

    def validate(self):
        """Custom validation for registration. Ensure that the supplied email
        address is not in use."""
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            self.email.errors.append('This email is already in use. Please \
                use another one.')
            return False

        return True
