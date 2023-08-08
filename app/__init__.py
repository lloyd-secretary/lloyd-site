import os
from flask import Flask, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.automap import automap_base

# Set this to True for production!
production = True

app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
db.Model = automap_base(db.Model)
from app import models
db.Model.prepare(db.engine, reflect=True)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'lloyd.login'
login_manager.login_message = None


from app.lloyd import lloyd
from app.rotation import rotation
app.register_blueprint(lloyd, url_prefix='/lloyd')
app.register_blueprint(rotation, url_prefix='/rotation')

@app.route('/')
def route_root():
	return redirect(url_for('lloyd.index'))

# for setting up SSL, needed to verify we own lloyd.caltech.edu
# see README for setting up SSL
@app.route('/.well-known/acme-challenge/<var>')
def route_acme(var):
    return send_from_directory("/var/www/app/lloyd/static/acme-challenge/",var)

from lloyd import views
from rotation import views
