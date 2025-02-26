# app/routes/menu_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.controllers.menu_controller import MenuController
from app.controllers.restaurant_controller import RestaurantController
from app.utils.forms import MenuItemForm
from app.utils.decorators import admin_required

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

@menu_bp.route('/add/<int:restaurant_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add(restaurant_id):
    restaurant = RestaurantController.get_restaurant(restaurant_id)
    form = MenuItemForm()
    
    if form.validate_on_submit():
        menu_item = MenuController.create_menu_item(form, restaurant_id)
        flash(f'Ítem {menu_item.name} agregado al menú correctamente.')
        return redirect(url_for('restaurant.detail', id=restaurant_id))
    
    return render_template('menu/form.html', form=form, title=f'Agregar Ítem al Menú de {restaurant.name}', restaurant=restaurant)

@menu_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    menu_item = MenuController.get_menu_item(id)
    form = MenuItemForm()
    
    if form.validate_on_submit():
        menu_item = MenuController.update_menu_item(menu_item, form)
        flash(f'Ítem {menu_item.name} actualizado correctamente.')
        return redirect(url_for('restaurant.detail', id=menu_item.restaurant_id))
    elif request.method == 'GET':
        form.name.data = menu_item.name
        form.description.data = menu_item.description
        form.price.data = menu_item.price
        form.category.data = menu_item.category
    
    return render_template('menu/form.html', form=form, title=f'Editar Ítem del Menú', restaurant=menu_item.restaurant)

@menu_bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    menu_item = MenuController.get_menu_item(id)
    restaurant_id = menu_item.restaurant_id
    
    if MenuController.delete_menu_item(menu_item):
        flash(f'Ítem {menu_item.name} eliminado correctamente.')
    
    return redirect(url_for('restaurant.detail', id=restaurant_id))