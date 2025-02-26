# app/routes/main_routes.py
from flask import Blueprint, render_template
from app.controllers.restaurant_controller import RestaurantController

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    print("index")
    restaurants = RestaurantController.get_all_restaurants()
    return render_template('home.html', restaurants=restaurants)
