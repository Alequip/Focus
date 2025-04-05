from flask import render_template, jsonify, request, Blueprint
from flask_login import login_required, current_user
from ..services.stats_service import StatsService

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/user')
@login_required
def user_stats():
    """Ver estadísticas del usuario actual."""
    stats = StatsService.get_user_stats(current_user.id)
    return render_template('user_stats.html', stats=stats)

@stats_bp.route('/game/<int:game_id>')
@login_required
def game_stats(game_id):
    """Ver estadísticas de un juego específico."""
    stats = StatsService.get_game_stats(game_id)
    return render_template('game_stats.html', stats=stats)

@stats_bp.route('/record', methods=['POST'])
@login_required
def record_gameplay():
    """API endpoint para registrar una partida."""
    data = request.get_json()
    gameplay = StatsService.record_game_play(
        user_id=current_user.id,
        game_id=data['game_id'],
        score=data.get('score'),
        duration=data.get('duration')
    )
    return jsonify({'success': True}), 200
