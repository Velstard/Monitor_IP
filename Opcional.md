#Ejecutar para crear un usuario de rango DM mediante codigo mediante python

from models import db
from log import User
from app import app
import bcrypt

# Crear un usuario DM
def create_dm_user():
    with app.app_context():
        # Datos del nuevo usuario
        username = "DM_user"
        password = "secure_password"
        role = "DM"  # Rol del usuario

        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"El usuario '{username}' ya existe.")
            return

        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Crear el nuevo usuario
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        print(f"Usuario '{username}' creado exitosamente con rol '{role}'.")

# Ejecutar la función para crear el usuario
if __name__ == "__main__":
    create_dm_user()
