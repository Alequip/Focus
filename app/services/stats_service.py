from datetime import datetime
from sqlalchemy import func
from ..models import db
from ..models.gameplay import GamePlay
from ..models.game import Game
from ..models.user import User

class StatsService:
    @staticmethod
    def record_game_play(user_id, game_id, score=None, duration=None):
        """
        Registrar una partida de juego.
        """
        gameplay = GamePlay(
            user_id=user_id,
            game_id=game_id,
            score=score,
            duration=duration
        )
        db.session.add(gameplay)
        db.session.commit()
        return gameplay

    @staticmethod
    def get_user_stats(user_id):
        """
        Obtener estadísticas de un usuario.
        """
        # Total de juegos jugados
        total_games = db.session.query(func.count(GamePlay.id)).filter_by(user_id=user_id).scalar()
        
        # Juego favorito (más jugado)
        favorite_game_id = db.session.query(
            GamePlay.game_id,
            func.count(GamePlay.id).label('count')
        ).filter_by(user_id=user_id).group_by(GamePlay.game_id)\
        .order_by(func.count(GamePlay.id).desc()).first()
        
        favorite_game = None
        if favorite_game_id:
            favorite_game = Game.query.get(favorite_game_id[0])
        
        # Mejores puntuaciones por juego
        best_scores = db.session.query(
            Game.title,
            func.max(GamePlay.score).label('best_score')
        ).join(GamePlay).filter(GamePlay.user_id == user_id)\
        .group_by(Game.id).all()
        
        # Tiempo total jugado
        total_time = db.session.query(func.sum(GamePlay.duration))\
        .filter_by(user_id=user_id).scalar() or 0
        
        return {
            'total_games_played': total_games,
            'favorite_game': favorite_game.title if favorite_game else None,
            'best_scores': {game: score for game, score in best_scores},
            'total_time_played': total_time
        }

    @staticmethod
    def get_game_stats(game_id):
        """
        Obtener estadísticas de un juego específico.
        """
        # Veces jugado
        times_played = db.session.query(func.count(GamePlay.id)).filter_by(game_id=game_id).scalar()
        
        # Puntuación promedio
        avg_score = db.session.query(func.avg(GamePlay.score))\
        .filter_by(game_id=game_id).scalar() or 0
        
        # Duración promedio
        avg_duration = db.session.query(func.avg(GamePlay.duration))\
        .filter_by(game_id=game_id).scalar() or 0
        
        # Mejores jugadores
        top_players = db.session.query(
            User.username,
            func.max(GamePlay.score).label('best_score')
        ).join(GamePlay).filter(GamePlay.game_id == game_id)\
        .group_by(User.id).order_by(func.max(GamePlay.score).desc()).limit(5).all()
        
        return {
            'times_played': times_played,
            'average_score': round(float(avg_score), 2),
            'average_duration': round(float(avg_duration), 2),
            'top_players': [(username, score) for username, score in top_players]
        }
