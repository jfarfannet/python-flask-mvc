# Crear archivo add_menu_items.py
from app import create_app, db
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem

app = create_app()

# Define los platos para cada restaurante
menu_items = {
    "Pizza Deliciosa": [
        {
            "name": "Pizza Margarita",
            "description": "Pizza clásica con salsa de tomate, mozzarella y albahaca fresca",
            "price": 9.99,
            "category": "Pizzas",
            "is_available": True
        },
        {
            "name": "Pizza Pepperoni",
            "description": "Pizza con abundante pepperoni y queso mozzarella",
            "price": 11.99,
            "category": "Pizzas",
            "is_available": True
        },
        {
            "name": "Ensalada César",
            "description": "Lechuga romana, crutones, parmesano y aderezo César",
            "price": 6.50,
            "category": "Entradas",
            "is_available": True
        },
        {
            "name": "Refresco",
            "description": "Bebida gaseosa de 500ml (varios sabores)",
            "price": 2.50,
            "category": "Bebidas",
            "is_available": True
        }
    ],
    "Burguer House": [
        {
            "name": "Hamburguesa Clásica",
            "description": "Carne de res, lechuga, tomate, cebolla y queso cheddar",
            "price": 8.99,
            "category": "Hamburguesas",
            "is_available": True
        },
        {
            "name": "Hamburguesa Doble",
            "description": "Doble carne, doble queso, bacon y salsa especial",
            "price": 12.99,
            "category": "Hamburguesas",
            "is_available": True
        },
        {
            "name": "Papas Fritas",
            "description": "Papas fritas crujientes con sal",
            "price": 3.50,
            "category": "Acompañamientos",
            "is_available": True
        },
        {
            "name": "Malteada",
            "description": "Malteada cremosa (chocolate, vainilla o fresa)",
            "price": 4.99,
            "category": "Bebidas",
            "is_available": True
        }
    ]
}

with app.app_context():
    for restaurant_name, items in menu_items.items():
        # Buscar el restaurante por nombre
        restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
        
        if restaurant:
            for item_data in items:
                # Verificar si el ítem ya existe
                existing = MenuItem.query.filter_by(
                    name=item_data["name"],
                    restaurant_id=restaurant.id
                ).first()
                
                if not existing:
                    # Crear nuevo ítem del menú
                    menu_item = MenuItem(
                        restaurant_id=restaurant.id,
                        **item_data
                    )
                    db.session.add(menu_item)
            
            print(f"Ítems agregados al menú de {restaurant_name}")
        else:
            print(f"Restaurante '{restaurant_name}' no encontrado")
    
    db.session.commit()
    print("¡Todos los ítems del menú han sido agregados correctamente!")