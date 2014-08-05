from flask_wtf import Form, RecaptchaField, Recaptcha
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo

from gamefolk.users.models import User

class LoginForm(Form):
    """Form to log in to the shop."""
    email = TextField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required()])

class RegisterForm(Form):
    """Form to register an account for the shop."""
    email = TextField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Confirm Password', [
        Required(),
        EqualTo('password', message='Passwords do not match.'),
        ])
    recaptcha = RecaptchaField(validators=[Recaptcha(message='The reCAPTCHA ' \
        'code you entered was incorrect. Please try again.')])

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
