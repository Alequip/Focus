from ..models import db
from ..models.user import User
from werkzeug.security import generate_password_hash

class UserService:
    @staticmethod
    def create_user(username, password, role='student'):
        """Crear un nuevo usuario."""
        user = User(
            username=username,
            role=role
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        """Obtener usuario por ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        """Obtener usuario por nombre de usuario."""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def update_user_role(user_id, new_role):
        """Actualizar el rol de un usuario."""
        user = User.query.get(user_id)
        if user and new_role in ['student', 'admin']:
            user.role = new_role
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_user(user_id):
        """Eliminar un usuario."""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_users():
        """Obtener todos los usuarios."""
        return User.query.all()

    @staticmethod
    def initialize_admin():
        """Inicializar usuario administrador si no existe."""
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            return admin
        return None
