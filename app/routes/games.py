from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import games_bp
from ..services.game_service import GameService

@games_bp.route('/')
@login_required
def games_selection():
    # Verificar si el usuario está autenticado (el decorador @login_required ya lo hace)
    # pero agregamos una verificación adicional
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Si es estudiante, mostrar la selección de juegos
    if current_user.role == 'student':
        return render_template('games_selection.html')
    
    # Si es admin, redirigir al dashboard
    return redirect(url_for('admin.dashboard'))

@games_bp.route('/<age_group>')
@login_required
def games_list(age_group):
    if current_user.role == 'student':
        games = GameService.get_games_by_age_group(age_group)
        return render_template('games_list.html', games=games, age_group=age_group)
    return redirect(url_for('admin.dashboard'))

@games_bp.route('/play/<int:game_id>')
@login_required
def play_game(game_id):
    game = GameService.get_game_by_id(game_id)
    if not game:
        return render_template('game_not_found.html')
    if game.title == "Aventura de Colores":
        return render_template('color_game.html')
    elif game.title == "Juego de Memoria":
        return render_template('memory_game.html')
    elif game.title == "Snake Game":
        return render_template('snake_game.html')
    return render_template('game_not_found.html')
