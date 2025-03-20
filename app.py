from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import pyodbc

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://@localhost/Inveing?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'student'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age_group = db.Column(db.String(20), nullable=False)  # '7-8', '9-10', '11-12'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)

with app.app_context():
    db.create_all()

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
            session['user'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        return 'Invalid Credentials'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        if session['role'] == 'admin':
            games = Game.query.all()
            return render_template('admin_dashboard.html', games=games)
        return render_template('student_dashboard.html')
    return redirect(url_for('login'))

@app.route('/games/<age_group>')
def games(age_group):
    if 'user' in session and session['role'] == 'student':
        games_list = Game.query.filter_by(age_group=age_group).all()
        return render_template('games.html', games=games_list, age_group=age_group)
    return redirect(url_for('login'))

@app.route('/add_game', methods=['POST'])
def add_game():
    if 'user' in session and session['role'] == 'admin':
        title = request.form['title']
        description = request.form['description']
        age_group = request.form['age_group']
        new_game = Game(title=title, description=description, age_group=age_group)
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/delete_game/<int:game_id>')
def delete_game(game_id):
    if 'user' in session and session['role'] == 'admin':
        game = Game.query.get(game_id)
        if game:
            db.session.delete(game)
            db.session.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        # Crear el nuevo usuario
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        
        # Guardar el usuario en la base de datos
        db.session.add(new_user)
        db.session.commit()
        
        # Redirigir a la página de login después de registrar al usuario
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
