from ..models import db
from ..models.game import Game

class GameService:
    @staticmethod
    def create_game(title, description, age_group):
        """Crear un nuevo juego."""
        game = Game(
            title=title,
            description=description,
            age_group=age_group
        )
        db.session.add(game)
        db.session.commit()
        return game

    @staticmethod
    def get_game_by_id(game_id):
        """Obtener juego por ID."""
        return Game.query.get(game_id)

    @staticmethod
    def get_games_by_age_group(age_group):
        """Obtener juegos por grupo de edad."""
        return Game.query.filter_by(age_group=age_group).all()

    @staticmethod
    def update_game(game_id, title=None, description=None, age_group=None):
        """Actualizar información de un juego."""
        game = Game.query.get(game_id)
        if game:
            if title:
                game.title = title
            if description:
                game.description = description
            if age_group:
                game.age_group = age_group
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_game(game_id):
        """Eliminar un juego."""
        game = Game.query.get(game_id)
        if game:
            db.session.delete(game)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_games():
        """Obtener todos los juegos."""
        return Game.query.all()

    @staticmethod
    def initialize_default_games():
        """Inicializar juegos por defecto si no existen."""
        if not Game.query.first():
            default_games = [
                {
                    'age_group': '7-8',
                    'title': 'Aventura de Colores',
                    'description': 'Un juego educativo para aprender los colores'
                },
                {
                    'age_group': '9-10',
                    'title': 'Juego de Memoria',
                    'description': 'Ejercita tu memoria encontrando pares de cartas'
                },
                {
                    'age_group': '11-12',
                    'title': 'Snake Game',
                    'description': '¡El clásico juego de la serpiente! Controla la serpiente y come la comida para crecer'
                }
            ]
            
            for game_data in default_games:
                game = Game(**game_data)
                db.session.add(game)
            
            db.session.commit()
            return True
        return False
