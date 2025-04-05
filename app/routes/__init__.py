from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)
games_bp = Blueprint('games', __name__)

from . import auth, admin, games, main
