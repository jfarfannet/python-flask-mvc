# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    # app = Flask(__name__)
    app = Flask(__name__, 
            template_folder='views/templates',
            static_folder='views/static')
    app.config.from_object(config_class)
    
    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Registrar blueprints
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.restaurant_routes import restaurant_bp
    from app.routes.menu_routes import menu_bp
    from app.routes.order_routes import order_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    
    return app