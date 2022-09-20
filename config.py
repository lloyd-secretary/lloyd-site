import os

SQLALCHEMY_DATABASE_URI = 'mysql://web@localhost:3306/lloyd'
SQLALCHEMY_BINDS = {
    'rotation':        'mysql://web@localhost:3306/rotation',
}
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = '\xa7\xe3\x800!|s\x80\x8e\x8e$\x90'

BCRYPT_LOG_ROUNDS = 12