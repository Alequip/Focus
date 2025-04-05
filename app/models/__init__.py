from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Importar modelos
from .user import User
from .game import Game
from .gameplay import GamePlay

def init_db(app):
    db.init_app(app)
