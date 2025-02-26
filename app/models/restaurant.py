# app/models/restaurant.py
from app import db

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(256))
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    delivery_time = db.Column(db.Integer)  # Tiempo estimado en minutos
    delivery_fee = db.Column(db.Float)
    rating = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relaciones
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy='dynamic')
    
    def __repr__(self):
        return f'<Restaurant {self.name}>'