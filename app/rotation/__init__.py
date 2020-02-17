from flask import Blueprint
from .. import production
from flask_cors import CORS

rotation = Blueprint('rotation', __name__, template_folder='templates', static_folder='static')

# Allow cross-origin resource sharing for API for development
if not production:
    CORS(rotation)

from . import views
from . import api