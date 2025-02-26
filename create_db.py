# Crea un archivo create_db.py en la raíz del proyecto
from app import create_app, db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.models.order import Order, OrderItem
from app.models.address import Address

app = create_app()

with app.app_context():
    db.create_all()
    print("Tablas creadas exitosamente")