from flask.ext.security import RegisterForm
from flask.ext.wtf import RecaptchaField, Recaptcha
from wtforms import PasswordField
from wtforms.validators import EqualTo, Required


class ExtendedRegisterForm(RegisterForm):
    """Form to register an account for the shop."""
    password_confirm = PasswordField('Confirm Password',
            [Required(), EqualTo('password', 'Passwords must match')])
    recaptcha_validator = Recaptcha(
        message='The reCAPTCHA code you entered was incorrect. '
                'Please try again.')
    recaptcha = RecaptchaField(validators=[recaptcha_validator])
