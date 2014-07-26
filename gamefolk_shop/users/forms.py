from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo

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
