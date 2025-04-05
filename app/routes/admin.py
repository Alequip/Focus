from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import admin_bp
from ..services.user_service import UserService
from ..services.game_service import GameService
from ..utils.decorators import admin_required
from ..models.user import User
from ..models import db

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = UserService.get_all_users()
    games = GameService.get_all_games()
    return render_template('admin_dashboard.html', users=users, games=games)

@admin_bp.route('/add_user', methods=['POST'])
@login_required
@admin_required
def add_user():
    username = request.form['username']
    password = request.form['password']
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash('Usuario agregado exitosamente')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes eliminar tu propio usuario')
        return redirect(url_for('admin.dashboard'))
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/set_user_role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def set_user_role(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes cambiar tu propio rol')
        return redirect(url_for('admin.dashboard'))
    role = request.form['role']
    if role not in ['admin', 'student']:
        flash('Rol inválido')
        return redirect(url_for('admin.dashboard'))
    user.role = role
    db.session.commit()
    flash('Rol actualizado exitosamente')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/add_game', methods=['POST'])
@login_required
@admin_required
def add_game():
    title = request.form['title']
    description = request.form['description']
    age_group = request.form['age_group']
    GameService.create_game(title, description, age_group)
    flash('Juego agregado exitosamente')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_game/<int:game_id>', methods=['POST'])
@login_required
@admin_required
def delete_game(game_id):
    game = GameService.get_game_by_id(game_id)
    if game:
        GameService.delete_game(game_id)
        flash('Juego eliminado exitosamente')
    else:
        flash('Juego no encontrado')
    return redirect(url_for('admin.dashboard'))
