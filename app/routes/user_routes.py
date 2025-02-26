# app/routes/user_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.controllers.user_controller import UserController
from app.utils.forms import ProfileForm, PasswordChangeForm, AddressForm

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        UserController.update_user_profile(form)
        flash('Perfil actualizado correctamente.')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone.data = current_user.phone
    return render_template('user/profile.html', form=form)

@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if UserController.change_password(form):
            flash('Contraseña actualizada correctamente.')
            return redirect(url_for('user.profile'))
        else:
            flash('La contraseña actual es incorrecta.')
    return render_template('user/change_password.html', form=form)

@user_bp.route('/addresses')
@login_required
def addresses():
    addresses = UserController.get_user_addresses()
    return render_template('user/addresses.html', addresses=addresses)

@user_bp.route('/address/add', methods=['GET', 'POST'])
@login_required
def add_address():
    form = AddressForm()
    if form.validate_on_submit():
        UserController.add_address(form)
        flash('Dirección agregada correctamente.')
        return redirect(url_for('user.addresses'))
    return render_template('user/address_form.html', form=form, title='Agregar Dirección')

@user_bp.route('/address/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_address(id):
    form = AddressForm()
    if form.validate_on_submit():
        address = UserController.update_address(id, form)
        if address:
            flash('Dirección actualizada correctamente.')
            return redirect(url_for('user.addresses'))
        else:
            flash('No tienes permiso para editar esta dirección.')
            return redirect(url_for('user.addresses'))
    elif request.method == 'GET':
        address = Address.query.get_or_404(id)
        if address.user_id != current_user.id:
            flash('No tienes permiso para editar esta dirección.')
            return redirect(url_for('user.addresses'))
        form.street.data = address.street
        form.city.data = address.city
        form.state.data = address.state
        form.zip_code.data = address.zip_code
        form.is_default.data = address.is_default
    return render_template('user/address_form.html', form=form, title='Editar Dirección')

@user_bp.route('/address/delete/<int:id>')
@login_required
def delete_address(id):
    if UserController.delete_address(id):
        flash('Dirección eliminada correctamente.')
    else:
        flash('No tienes permiso para eliminar esta dirección.')
    return redirect(url_for('user.addresses'))