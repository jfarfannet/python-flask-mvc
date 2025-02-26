# app/controllers/auth_controller.py
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_user, logout_user, current_user
from app.models.user import User
from app import db

class AuthController:
    @staticmethod
    def login(form):
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.index'))
            flash('Email o contraseña incorrectos')
        return render_template('auth/login.html', form=form)
    
    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('main.index'))
    
    @staticmethod
    def register(form):
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect(url_for('auth.login'))
        return render_template('auth/register.html', form=form)