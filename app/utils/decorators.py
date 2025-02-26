# app/utils/decorators.py
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Se requieren permisos de administrador para acceder a esta página.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function