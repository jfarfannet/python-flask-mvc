python -m venv venv
venv\Scripts\activate
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

ejecutar
python create_db.py
python create_admin.py
create_restaurants.py
add_menu_items.py
