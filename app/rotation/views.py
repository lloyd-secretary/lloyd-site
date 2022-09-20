import sys
from flask import render_template, g, send_from_directory, flash, redirect, session, url_for, request

from flask_login import login_required, current_user
from . import rotation
from .. import db, login_manager
from ..models import *
from forms import *


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# validate all rotation users before serving any page
@rotation.before_request
def before_request():
    if current_user.is_authenticated:
        g.user = current_user
    else:
        return redirect(url_for('lloyd.login'))
    # require user.rotation to see any pages
    if not (g.user.rotation):
        return redirect(url_for('lloyd.index'))
    
    print(g.user, file=sys.stderr)

    #if g.user.membership == 's':
    #    return redirect(url_for('lloyd.index'))

def is_admin():
    return g.user.admin

@rotation.route('/')
@login_required
def rotation_home():
    return render_template("rotationUI.html")

@rotation.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img/', path)
