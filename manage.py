from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app, db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.models.order import Order, OrderItem
from app.models.address import Address

app = create_app()

# Alternativa sin Flask-Script para versiones más recientes de Flask
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Esto creará directamente las tablas sin migraciones
        print("Tablas creadas exitosamente")