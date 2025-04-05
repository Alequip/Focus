from datetime import datetime
from . import db

class GamePlay(db.Model):
    """Modelo para registrar las partidas jugadas."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # duración en segundos
    completed = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    user = db.relationship('User', backref=db.backref('gameplays', lazy=True))
    game = db.relationship('Game', backref=db.backref('gameplays', lazy=True))
