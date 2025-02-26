# app/controllers/restaurant_controller.py
from flask import request, current_app
from app.models.restaurant import Restaurant
from app import db

class RestaurantController:
    @staticmethod
    def get_all_restaurants():
        page = request.args.get('page', 1, type=int)
        restaurants = Restaurant.query.filter_by(is_active=True).paginate(
            page=page, 
            per_page=current_app.config['RESTAURANTS_PER_PAGE'],
            error_out=False
        )
        return restaurants
    
    @staticmethod
    def get_restaurant(id):
        return Restaurant.query.get_or_404(id)
    
    @staticmethod
    def create_restaurant(form):
        restaurant = Restaurant(
            name=form.name.data,
            description=form.description.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data,
            delivery_time=form.delivery_time.data,
            delivery_fee=form.delivery_fee.data
        )
        if form.image.data:
            # Lógica para subir y guardar la imagen
            pass
        
        db.session.add(restaurant)
        db.session.commit()
        return restaurant
    
    @staticmethod
    def update_restaurant(restaurant, form):
        restaurant.name = form.name.data
        restaurant.description = form.description.data
        restaurant.address = form.address.data
        restaurant.phone = form.phone.data
        restaurant.email = form.email.data
        restaurant.delivery_time = form.delivery_time.data
        restaurant.delivery_fee = form.delivery_fee.data
        
        if form.image.data:
            # Lógica para subir y actualizar la imagen
            pass
        
        db.session.commit()
        return restaurant
    
    @staticmethod
    def delete_restaurant(restaurant):
        restaurant.is_active = False
        db.session.commit()
        return True
