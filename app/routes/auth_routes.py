# app/routes/auth_routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.controllers.auth_controller import AuthController
from app.utils.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    return AuthController.login(form)

@auth_bp.route('/logout')
@login_required
def logout():
    return AuthController.logout()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    return AuthController.register(form)