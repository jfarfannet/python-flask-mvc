# app/controllers/order_controller.py
from datetime import datetime
from flask_login import current_user
from app.models.order import Order, OrderItem
from app.models.menu import MenuItem
from app import db

class OrderController:
    @staticmethod
    def get_user_orders(user_id):
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    @staticmethod
    def get_order(id):
        return Order.query.get_or_404(id)
    
    @staticmethod
    def create_order(cart, restaurant_id, address_id, payment_method):
        # Crear nueva orden
        order = Order(
            user_id=current_user.id,
            restaurant_id=restaurant_id,
            address_id=address_id,
            payment_method=payment_method,
            status='pending',
            created_at=datetime.utcnow()
        )
        
        # Obtener el restaurante y asignar la tarifa de entrega
        from app.models.restaurant import Restaurant
        restaurant = Restaurant.query.get(restaurant_id)
        order.delivery_fee = restaurant.delivery_fee
        
        db.session.add(order)
        db.session.flush()  # Para obtener el ID de la orden
        
        # Agregar items a la orden
        for item_id, quantity in cart.items():
            menu_item = MenuItem.query.get(item_id)
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=quantity,
                price=menu_item.price
            )
            db.session.add(order_item)
        
        # Calcular el total
        order.calculate_total()
        
        db.session.commit()
        return order
    
    @staticmethod
    def update_order_status(order, status):
        order.status = status
        order.updated_at = datetime.utcnow()
        db.session.commit()
        return order
    
    @staticmethod
    def cancel_order(order):
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        return False