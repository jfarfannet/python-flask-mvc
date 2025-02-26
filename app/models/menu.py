# app/models/menu.py
from app import db

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_url = db.Column(db.String(256))
    category = db.Column(db.String(64))
    is_available = db.Column(db.Boolean, default=True)
    
    # Relaciones
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    order_items = db.relationship('OrderItem', backref='menu_item', lazy='dynamic')
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'