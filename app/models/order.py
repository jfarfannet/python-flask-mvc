# app/models/order.py
from datetime import datetime
from app import db

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, preparing, on_way, delivered, cancelled
    total_amount = db.Column(db.Float)
    delivery_fee = db.Column(db.Float)
    payment_method = db.Column(db.String(20))  # cash, credit_card, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    items = db.relationship('OrderItem', backref='order', lazy='dynamic')
    restaurant = db.relationship('Restaurant')
    delivery_address = db.relationship('Address')
    
    def calculate_total(self):
        items_total = sum(item.quantity * item.price for item in self.items)
        self.total_amount = items_total + self.delivery_fee
        return self.total_amount
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)  # Precio en el momento de la orden
    special_instructions = db.Column(db.Text)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'