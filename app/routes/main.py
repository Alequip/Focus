from flask import Blueprint, redirect, url_for, session
from flask_login import current_user, logout_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Forzar cierre de sesión si hay inconsistencias
    if not current_user.is_authenticated or 'user' not in session:
        if current_user.is_authenticated:
            logout_user()
        session.clear()
        return redirect(url_for('auth.login'))
    
    # Verificar que el usuario en sesión coincida
    if session.get('user') != current_user.username:
        logout_user()
        session.clear()
        return redirect(url_for('auth.login'))
    
    # Redirigir según el rol
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('games.games_selection'))
