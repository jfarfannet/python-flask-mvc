# app/controllers/menu_controller.py
from app.models.menu import MenuItem
from app import db

class MenuController:
    @staticmethod
    def get_menu_by_restaurant(restaurant_id):
        return MenuItem.query.filter_by(restaurant_id=restaurant_id, is_available=True).all()
    
    @staticmethod
    def get_menu_item(id):
        return MenuItem.query.get_or_404(id)
    
    @staticmethod
    def create_menu_item(form, restaurant_id):
        menu_item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            restaurant_id=restaurant_id
        )
        if form.image.data:
            # Lógica para subir y guardar la imagen
            pass
        
        db.session.add(menu_item)
        db.session.commit()
        return menu_item
    
    @staticmethod
    def update_menu_item(menu_item, form):
        menu_item.name = form.name.data
        menu_item.description = form.description.data
        menu_item.price = form.price.data
        menu_item.category = form.category.data
        
        if form.image.data:
            # Lógica para subir y actualizar la imagen
            pass
        
        db.session.commit()
        return menu_item
    
    @staticmethod
    def delete_menu_item(menu_item):
        menu_item.is_available = False
        db.session.commit()
        return True
