from . import db

class Game(db.Model):
    """Game model for educational games."""
    
    id = db.Column(db.Integer, primary_key=True)
    age_group = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<Game {self.title}>'
