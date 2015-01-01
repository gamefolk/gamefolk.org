CSRF_ENABLED = True

# Security Settings
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_CONFIRMABLE = True

SECURITY_PASSWORD_HASH = 'bcrypt'

SECURITY_MSG_INVALID_PASSWORD = ('Username and password do not match', 'error')
SECURITY_MSG_PASSWORD_NOT_PROVIDED = ('Username and password do not match', 'error')
SECURITY_MSG_USER_DOES_NOT_EXIST = ('Username and password do not match', 'error')

SECURITY_EMAIL_SENDER = 'donotreply@gamefolk.org'
SECURITY_EMAIL_SUBJECT_REGISTER = 'Gamefolk.org Registration Confirmation'
