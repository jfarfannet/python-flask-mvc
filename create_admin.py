from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Verificar si el usuario admin ya existe
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            phone='123456789',
            is_admin=True
        )
        admin.set_password('admin123')  # Por seguridad, cambia esta contraseña
        db.session.add(admin)
        db.session.commit()
        print("¡Usuario administrador creado exitosamente!")
    else:
        print("El usuario administrador ya existe.")