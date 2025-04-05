from flask import Flask
from flask_login import LoginManager
from config import config
from .models import init_db, db
from .models.user import User
from .routes import auth_bp, admin_bp, games_bp
from .routes.main import main_bp
from .routes.stats import stats_bp

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Ensure secret key is set
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = 'dev-key-please-change-in-production'

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(games_bp, url_prefix='/games')
    app.register_blueprint(stats_bp, url_prefix='/stats')

    # Create database tables
    with app.app_context():
        db.create_all()
        init_database(db)

    return app

def init_database(db):
    """Initialize database with admin user and games"""
    from werkzeug.security import generate_password_hash
    
    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)

    # Initialize games
    from .models.game import Game
    if not Game.query.first():
        games = [
            Game(
                age_group='7-8',
                title='Aventura de Colores',
                description='Un juego educativo para aprender los colores'
            ),
            Game(
                age_group='9-10',
                title='Juego de Memoria',
                description='Ejercita tu memoria encontrando pares de cartas'
            ),
            Game(
                age_group='11-12',
                title='Snake Game',
                description='¡El clásico juego de la serpiente! Controla la serpiente y come la comida para crecer'
            )
        ]
        for game in games:
            db.session.add(game)

    db.session.commit()
