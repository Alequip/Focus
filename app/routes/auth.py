from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from ..services.user_service import UserService

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Limpiar la sesión anterior
    session.clear()
    
    # Si ya está autenticado, redirigir según el rol
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('games.games_selection'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserService.get_user_by_username(username)
        
        if user and user.check_password(password):
            # Configurar la sesión como permanente
            session.permanent = True
            
            # Iniciar sesión
            login_user(user)
            
            # Guardar datos en la sesión
            session['user'] = user.username
            session['role'] = user.role
            
            # Redirigir según el rol
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('games.games_selection'))
            
        flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if UserService.get_user_by_username(username):
            flash('Username already exists')
            return render_template('register.html')
        UserService.create_user(username, password, 'student')
        return redirect(url_for('auth.login'))
    return render_template('register.html')
