from app import create_app
from flask_login import LoginManager, current_user, logout_user
from app.models.user import User
from datetime import timedelta
from flask import session, redirect, url_for

app = create_app()

# Configuración de seguridad
app.config.update(
    SESSION_COOKIE_SECURE=False,  
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_REFRESH_EACH_REQUEST=True,
    SESSION_PROTECTION='strong'
)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'
login_manager.refresh_view = 'auth.login'
login_manager.needs_refresh_message = 'Por favor inicia sesión nuevamente para verificar tu identidad'
login_manager.needs_refresh_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    if 'user' not in session:
        return None
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    # Forzar cierre de sesión si hay inconsistencias
    if 'user' not in session and hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        logout_user()
        return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='127.0.0.1', port=5000)
