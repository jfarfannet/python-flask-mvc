# app/controllers/user_controller.py
from flask_login import current_user
from app.models.user import User
from app.models.address import Address
from app import db

class UserController:
    @staticmethod
    def get_user_profile(user_id):
        return User.query.get_or_404(user_id)
    
    @staticmethod
    def update_user_profile(form):
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        
        db.session.commit()
        return current_user
    
    @staticmethod
    def change_password(form):
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_user_addresses():
        return Address.query.filter_by(user_id=current_user.id).all()
    
    @staticmethod
    def add_address(form):
        # Si es la primera dirección o se marca como predeterminada
        if form.is_default.data:
            # Desmarcar otras direcciones predeterminadas
            Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
        
        address = Address(
            user_id=current_user.id,
            street=form.street.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            is_default=form.is_default.data
        )
        
        db.session.add(address)
        db.session.commit()
        return address
    
    @staticmethod
    def update_address(address_id, form):
        address = Address.query.get_or_404(address_id)
        
        # Verificar propiedad de la dirección
        if address.user_id != current_user.id:
            return None
        
        # Si se marca como predeterminada
        if form.is_default.data and not address.is_default:
            # Desmarcar otras direcciones predeterminadas
            Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
        
        address.street = form.street.data
        address.city = form.city.data
        address.state = form.state.data
        address.zip_code = form.zip_code.data
        address.is_default = form.is_default.data
        
        db.session.commit()
        return address
    
    @staticmethod
    def delete_address(address_id):
        address = Address.query.get_or_404(address_id)
        
        # Verificar propiedad de la dirección
        if address.user_id != current_user.id:
            return False
        
        db.session.delete(address)
        db.session.commit()
        return True