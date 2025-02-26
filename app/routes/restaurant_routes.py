# app/routes/restaurant_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.controllers.restaurant_controller import RestaurantController
from app.controllers.menu_controller import MenuController
from app.utils.forms import RestaurantForm
from app.utils.decorators import admin_required

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurants')

@restaurant_bp.route('/')
def index():
    restaurants = RestaurantController.get_all_restaurants()
    return render_template('restaurants/list.html', restaurants=restaurants)

@restaurant_bp.route('/<int:id>')
def detail(id):
    restaurant = RestaurantController.get_restaurant(id)
    menu_items = MenuController.get_menu_by_restaurant(id)
    return render_template('restaurants/detail.html', restaurant=restaurant, menu_items=menu_items)

@restaurant_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    form = RestaurantForm()
    if form.validate_on_submit():
        restaurant = RestaurantController.create_restaurant(form)
        flash(f'Restaurante {restaurant.name} creado correctamente.')
        return redirect(url_for('restaurant.index'))
    return render_template('restaurants/form.html', form=form, title='Agregar Restaurante')

@restaurant_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    restaurant = RestaurantController.get_restaurant(id)
    form = RestaurantForm()
    
    if form.validate_on_submit():
        restaurant = RestaurantController.update_restaurant(restaurant, form)
        flash(f'Restaurante {restaurant.name} actualizado correctamente.')
        return redirect(url_for('restaurant.detail', id=restaurant.id))
    elif request.method == 'GET':
        form.name.data = restaurant.name
        form.description.data = restaurant.description
        form.address.data = restaurant.address
        form.phone.data = restaurant.phone
        form.email.data = restaurant.email
        form.delivery_time.data = restaurant.delivery_time
        form.delivery_fee.data = restaurant.delivery_fee
    
    return render_template('restaurants/form.html', form=form, title='Editar Restaurante')

@restaurant_bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    restaurant = RestaurantController.get_restaurant(id)
    if RestaurantController.delete_restaurant(restaurant):
        flash(f'Restaurante {restaurant.name} eliminado correctamente.')
    return redirect(url_for('restaurant.index'))