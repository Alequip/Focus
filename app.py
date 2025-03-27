from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inveing.db'
db = SQLAlchemy(app)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Specify the login view function

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='student')  # 'admin' or 'student'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age_group = db.Column(db.String(20), nullable=False)  # '7-8', '9-10', '11-12'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)  # Log in the user using Flask-Login
            session['user'] = user.username #redundante, pero se deja
            session['role'] = user.role #redundante, pero se deja
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')  # Use flash for error messages
        return render_template('login.html')
    return render_template('login.html')

def is_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        abort(403)  # Forbidden

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        users = User.query.all()
        games = Game.query.all() #get games
        return render_template('admin_dashboard.html', users=users, games=games)
    return render_template('student_dashboard.html')

@app.route('/games/<age_group>')
@login_required
def games(age_group):
    if current_user.role == 'student':
        games_list = Game.query.filter_by(age_group=age_group).all()
        return render_template('games.html', games=games_list, age_group=age_group)
    return redirect(url_for('dashboard')) #redirect a dashboard

@app.route('/add_game', methods=['POST'])
@login_required
def add_game():
    is_admin()
    title = request.form['title']
    description = request.form['description']
    age_group = request.form['age_group']
    new_game = Game(title=title, description=description, age_group=age_group)
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_game/<int:game_id>')
@login_required
def delete_game(game_id):
    is_admin()
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required #Require Login
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role='student')  # Set default role
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin/user/<int:user_id>/set_role', methods=['POST'])
@login_required
def set_user_role(user_id):
    is_admin()
    user = User.query.get_or_404(user_id)
    new_role = request.form['role']
    if new_role in ('student', 'admin'):
        user.role = new_role
        db.session.commit()
    else:
        flash('Invalid role.')
    return redirect(url_for('dashboard'))

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    is_admin()
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/play_game/<int:game_id>')
def play_game(game_id):
    game = Game.query.get(game_id)
    if game:
        print(f"Título del juego: {game.title}")  # Para debug
        if game.title == "Aventura de Colores":
            return redirect(url_for('color_game'))
        elif game.title == "Juego de Memoria":
            return redirect(url_for('memory_game'))
        elif game.title == "Snake Game":
            return redirect(url_for('snake_game'))
        return f"Juego no implementado aún: {game.title}", 404
    else:
        return "Juego no encontrado", 404

@app.route('/color_game')
def color_game():
    return render_template('color_game.html')

@app.route('/memory_game')
@login_required
def memory_game():
    return render_template('memory_game.html')

@app.route('/snake_game')
@login_required
def snake_game():
    return render_template('snake_game.html')

with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
    
    # Eliminar todos los juegos existentes y crear nuevos
    Game.query.delete()
    games = [
        Game(age_group='7-8', title='Aventura de Colores', description='Un juego educativo para aprender los colores'),
        Game(age_group='9-10', title='Juego de Memoria', description='Ejercita tu memoria encontrando pares de cartas'),
        Game(age_group='11-12', title='Snake Game', description='¡El clásico juego de la serpiente! Controla la serpiente y come la comida para crecer')
    ]
    for game in games:
        db.session.add(game)
    
    db.session.commit()
if __name__ == '__main__':
    app.run(debug=True)
