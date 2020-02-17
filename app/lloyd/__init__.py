from flask import Blueprint

lloyd = Blueprint('lloyd', __name__, template_folder='templates', static_folder='static')

from . import views