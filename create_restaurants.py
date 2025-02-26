# Crea un archivo create_restaurants.py
from app import create_app, db
from app.models.restaurant import Restaurant

app = create_app()

restaurants = [
    {
        "name": "Pizza Deliciosa",
        "description": "Las mejores pizzas de la ciudad con ingredientes frescos y masa artesanal.",
        "address": "Calle Principal 123",
        "phone": "555-1234",
        "email": "info@pizzadeliciosa.com",
        "delivery_time": 30,
        "delivery_fee": 3.50,
        "rating": 4.5,
        "is_active": True
    },
    {
        "name": "Burguer House",
        "description": "Hamburguesas gourmet con carne 100% de res y pan recién horneado.",
        "address": "Avenida Central 456",
        "phone": "555-5678",
        "email": "contact@burguerhouse.com",
        "delivery_time": 25,
        "delivery_fee": 4.00,
        "rating": 4.2,
        "is_active": True
    },
    # Puedes agregar más restaurantes aquí
]

with app.app_context():
    for restaurant_data in restaurants:
        # Verificar si el restaurante ya existe
        existing = Restaurant.query.filter_by(name=restaurant_data["name"]).first()
        if not existing:
            restaurant = Restaurant(**restaurant_data)
            db.session.add(restaurant)
        
    db.session.commit()
    print("¡Restaurantes añadidos correctamente!")