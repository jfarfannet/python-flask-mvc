# app/routes/order_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app.controllers.order_controller import OrderController
from app.controllers.restaurant_controller import RestaurantController
from app.controllers.menu_controller import MenuController
from app.controllers.user_controller import UserController
from app.utils.forms import CheckoutForm

order_bp = Blueprint('order', __name__, url_prefix='/orders')

# Inicializar carrito en la sesión
@order_bp.before_app_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = {}
        session['restaurant_id'] = None

@order_bp.route('/')
@login_required
def index():
    orders = OrderController.get_user_orders(current_user.id)
    return render_template('orders/history.html', orders=orders)

@order_bp.route('/<int:id>')
@login_required
def detail(id):
    order = OrderController.get_order(id)
    if order.user_id != current_user.id:
        flash('No tienes permiso para ver este pedido.')
        return redirect(url_for('order.index'))
    return render_template('orders/detail.html', order=order)

@order_bp.route('/add-to-cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    menu_item = MenuController.get_menu_item(item_id)
    quantity = int(request.form.get('quantity', 1))
    
    # Si el carrito está vacío o es de otro restaurante, reiniciar
    if not session.get('restaurant_id') or session['restaurant_id'] != menu_item.restaurant_id:
        session['cart'] = {}
        session['restaurant_id'] = menu_item.restaurant_id
    
    # Agregar o actualizar ítem en el carrito
    if str(item_id) in session['cart']:
        session['cart'][str(item_id)] += quantity
    else:
        session['cart'][str(item_id)] = quantity
    
    session.modified = True
    flash(f'{menu_item.name} agregado al carrito.')
    return redirect(url_for('restaurant.detail', id=menu_item.restaurant_id))

@order_bp.route('/remove-from-cart/<int:item_id>')
def remove_from_cart(item_id):
    if str(item_id) in session['cart']:
        del session['cart'][str(item_id)]
        session.modified = True
    
    if not session['cart']:
        session['restaurant_id'] = None
    
    return redirect(url_for('order.cart'))

@order_bp.route('/update-cart', methods=['POST'])
def update_cart():
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            item_id = key.split('_')[1]
            quantity = int(value)
            
            if quantity > 0:
                session['cart'][item_id] = quantity
            else:
                del session['cart'][item_id]
    
    session.modified = True
    flash('Carrito actualizado correctamente.')
    return redirect(url_for('order.cart'))

@order_bp.route('/cart')
def cart():
    cart_items = []
    total = 0
    restaurant = None
    
    if session.get('restaurant_id'):
        restaurant = RestaurantController.get_restaurant(session['restaurant_id'])
        
        for item_id, quantity in session['cart'].items():
            menu_item = MenuController.get_menu_item(int(item_id))
            subtotal = menu_item.price * quantity
            total += subtotal
            
            cart_items.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'quantity': quantity,
                'subtotal': subtotal
            })
    
    return render_template('orders/cart.html', cart_items=cart_items, total=total, restaurant=restaurant)

@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # Verificar si hay items en el carrito
    if not session.get('cart') or not session.get('restaurant_id'):
        flash('Tu carrito está vacío.')
        return redirect(url_for('order.cart'))
    
    form = CheckoutForm()
    addresses = UserController.get_user_addresses()
    
    # Configurar las opciones del formulario con las direcciones del usuario
    form.address_id.choices = [(a.id, f"{a.street}, {a.city}, {a.state}, {a.zip_code}") for a in addresses]
    
    # Si no hay direcciones, redirigir para agregar una
    if not addresses:
        flash('Necesitas agregar una dirección antes de realizar un pedido.')
        return redirect(url_for('user.add_address'))
    
    if form.validate_on_submit():
        # Crear el pedido
        order = OrderController.create_order(
            session['cart'],
            session['restaurant_id'],
            form.address_id.data,
            form.payment_method.data
        )
        
        # Limpiar el carrito
        session['cart'] = {}
        session['restaurant_id'] = None
        
        flash('¡Pedido realizado con éxito!')
        return redirect(url_for('order.detail', id=order.id))
    
    # Calcular el total para mostrar en el formulario
    cart_items = []
    subtotal = 0
    restaurant = RestaurantController.get_restaurant(session['restaurant_id'])
    
    for item_id, quantity in session['cart'].items():
        menu_item = MenuController.get_menu_item(int(item_id))
        item_subtotal = menu_item.price * quantity
        subtotal += item_subtotal
        
        cart_items.append({
            'id': menu_item.id,
            'name': menu_item.name,
            'price': menu_item.price,
            'quantity': quantity,
            'subtotal': item_subtotal
        })
    
    total = subtotal + restaurant.delivery_fee
    
    return render_template(
        'orders/checkout.html', 
        form=form, 
        cart_items=cart_items, 
        subtotal=subtotal,
        delivery_fee=restaurant.delivery_fee,
        total=total,
        restaurant=restaurant
    )

@order_bp.route('/cancel/<int:id>')
@login_required
def cancel(id):
    order = OrderController.get_order(id)
    
    if order.user_id != current_user.id:
        flash('No tienes permiso para cancelar este pedido.')
        return redirect(url_for('order.index'))
    
    if OrderController.cancel_order(order):
        flash('Pedido cancelado exitosamente.')
    else:
        flash('No se puede cancelar este pedido porque ya está en proceso de entrega.')
    
    return redirect(url_for('order.detail', id=id))