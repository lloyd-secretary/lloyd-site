import os

SQLALCHEMY_DATABASE_URI = 'mysql://web@localhost/lloyd?charset=utf8mb4'
SQLALCHEMY_BINDS = {
    'rotation2025': 'mysql://web@localhost/rotation2025?charset=utf8mb4',
}
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = '\xa7\xe3\x800!|s\x80\x8e\x8e$\x90'

BCRYPT_LOG_ROUNDS = 12

