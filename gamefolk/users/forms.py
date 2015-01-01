from flask.ext.security import RegisterForm
from flask.ext.wtf import RecaptchaField, Recaptcha


class ExtendedRegisterForm(RegisterForm):
    """Form to register an account for the shop."""
    recaptcha_validator = Recaptcha(
        message='The reCAPTCHA code you entered was incorrect. '
                'Please try again.')
    recaptcha = RecaptchaField(validators=[recaptcha_validator])
