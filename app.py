# Bibliotecas importadas

import os # Para ejecutar comandos del sistema operativo
import smtplib # Para enviar correos electrónicos
import time # Para manejar el tiempo de espera entre pings
from email.mime.text import MIMEText # Para crear el cuerpo del correo electrónico
from email.mime.multipart import MIMEMultipart # Para crear correos electrónicos con múltiples partes
from flask import Flask, render_template, request, redirect, jsonify, flash, get_flashed_messages, session # Para manejar la aplicación web y las sesiones
import json # Para manejar datos en formato JSON
import threading # Para manejar hilos
from datetime import datetime  # Importar módulo para manejar fechas y horas
from flask_sqlalchemy import SQLAlchemy # Para manejar la base de datos
from werkzeug.security import generate_password_hash, check_password_hash # Para encriptar y verificar contraseñas
import secrets  # Importar biblioteca para generar tokens
from functools import wraps # Para crear decoradores
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Obtener la contraseña adicional para eliminar DM
#Para esto, tendras que crearte una variable de entorno en tu computadora,
#llamarla como DM_DELETE_PASSWORD y asignarle una contraseña que solo tu sepas
#Esta contraseña es para eliminar un DM o editarlo 
DM_DELETE_PASSWORD = os.getenv("DB_Password")

# Configuración de Flask
app = Flask(__name__)
app.secret_key = "Dgp*2025"  # Clave secreta para usar mensajes flash
app.debug = True

# Configuración de la base de datos PostgreSQL Esto es un ORM que se me hizo mas faicl manejar

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1254@localhost:5432/monitordb' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Modelo para las IPs. Si quiero agregar algun otro campo o agregar alguna otra funcion o cosa
#primero y siempre tengo que tocar esta parte, ademas de que tambien influye en la base de datos
class IP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

# Modelo para los usuarios
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="viewer")
    approved = db.Column(db.Boolean, default=False)  # Campo para aprobación

# Creacion de las tablas en la base de datos
with app.app_context():
    db.create_all()

# Función para enviar correos electrónicos, utilizando el servidor SMTP de Gmail con una contrase1ña generada
#por el mismo google app
def send_email(email_string):
    try:
        # Obtener los correos electrónicos de los usuarios con el rol "DM"
        dm_users = Users.query.filter_by(role="DM", approved=True).all()
        email_to_list = [user.email for user in dm_users]

        if not email_to_list:
            print("No hay usuarios DM aprobados para enviar correos.")  # Depuración
            return

        email_from = 'pasaporteserveralert@gmail.com'
        password = 'toxlyuttzgqbmhsb'
        subject = "Estado del IP/Host"

        for email_to in email_to_list:
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = email_to
            msg['Subject'] = subject
            msg.attach(MIMEText(email_string, 'plain', 'utf-8'))

            smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp_server.login(email_from, password)
            smtp_server.sendmail(email_from, email_to, msg.as_string())
            smtp_server.close()

            print(f"Correo enviado exitosamente a {email_to}.")  # Depuración
    except Exception as e:
        print(f"Error al enviar el correo: {e}")  # Mostrar el error en la consola (tengo )

# Función para monitorear las IPs
def monitor_ips():
    with app.app_context():  # Activar el contexto de la aplicación
        previous_status = {}  # Diccionario para almacenar el estado anterior de las IPs

        while True:
            try:
                print(f"Monitoreo iniciado: {datetime.now()}")  # Depuración
                ip_list = IP.query.all()  # Obtener todas las IPs de la base de datos
                current_status = {}  # Diccionario para almacenar el estado actual de las IPs

                for ip in ip_list:
                    # Realizar un ping a la IP
                    print(f"Ping a la IP: {ip.address}")  # Depuración
                    status = os.system(f"ping -n 1 {ip.address} >nul 2>&1")
                    if status != 0:
                        current_status[ip.address] = "inactiva"  # Registrar el estado actual como caída
                    else:
                        current_status[ip.address] = "activa"  # Registrar el estado actual como activa

                    # Actualizar el estado en la base de datos si ha cambiado
                    if ip.status != current_status[ip.address]:
                        print(f"Actualizando estado de {ip.address} a {current_status[ip.address]}")  # Depuración
                        ip.status = current_status[ip.address]
                        db.session.commit()  # Guardar los cambios en la base de datos

                # Comparar el estado actual con el estado anterior
                for ip_address, status in current_status.items():
                    if ip_address in previous_status:
                        # Si la IP estaba activa y ahora está caída, enviar un correo inmediatamente
                        if previous_status[ip_address] == "activa" and status == "inactiva":
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                            send_email(f"Hola, Este es un mensaje de notificación sobre el estado de las IPs monitoreadas.los DM : La IP {ip_address} estaba activa y ahora está caída.\nHora de caída: {timestamp}")
                        # Si la IP estaba inactiva y ahora está activa, enviar un correo
                        elif previous_status[ip_address] == "inactiva" and status == "activa":
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                            send_email(f"NOTIFICACIÓN: La IP {ip_address} estaba inactiva y ahora está activa.\nHora de activación: {timestamp}")

                # Actualizar el estado anterior con el estado actual
                previous_status = current_status

            except Exception as e:
                print(f"Error en el monitoreo: {e}")
                # Opcional: Marcar todas las IPs como inactivas si ocurre un error
                ip_list = IP.query.all()
                for ip in ip_list:
                    ip.status = "inactiva"
                db.session.commit()

            time.sleep(300)  # Esperar 5 minutos antes de volver a monitorear

# Credenciales de acceso (puedes mover esto a una base de datos o archivo de configuración)
USERNAME = "admin"
PASSWORD = "password123"

# Función para generar un token encriptado
def generate_encrypted_token():
    token = secrets.token_hex(32)  # Generar un token aleatorio de 32 bytes
    encrypted_token = generate_password_hash(token, method="pbkdf2:sha256")  # Encriptar el token
    return token, encrypted_token

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = Users.query.filter_by(username=session.get("user")).first()
            if not user or user.role not in allowed_roles:
                print(f"Acceso denegado para el usuario: {session.get('user')}")  # Depuración
                flash("No tienes permiso para realizar esta acción.", "error")
                return redirect("/")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Ruta para el registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "viewer")

        # Verificar si el usuario o el correo ya existen
        existing_user = Users.query.filter_by(username=username).first()
        existing_email = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("El nombre de usuario ya está en uso.", "error")
            return redirect("/register")
        if existing_email:
            flash("El correo electrónico ya está en uso.", "error")
            return redirect("/register")

        # Crear un nuevo usuario con contraseña encriptada
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = Users(username=username, email=email, password=hashed_password, role=role, approved=False)
        db.session.add(new_user)
        db.session.commit()

        # Mensaje flash para informar al usuario
        flash("Registro exitoso. Tu cuenta está pendiente de aprobación por un administrador o DM.", "success")
        return redirect("/register")

    return render_template("register.html")

# Ruta para el login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verificar si el usuario existe
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if not user.approved:
                flash("Tu cuenta está pendiente de aprobación por un administrador.", "error")
                return redirect("/login")  # Redirigir de vuelta al login si no está aprobado

            # Guardar el usuario en la sesión
            session["user"] = username
            flash("Inicio de sesión exitoso.", "success")
            return redirect("/status")  # Redirigir al área de estado

        # Si las credenciales son incorrectas
        flash("Usuario o contraseña incorrectos.", "error")
        return redirect("/login")

    return render_template("login.html")

# Modificar el middleware para verificar la sesión
@app.before_request
def require_login():
    allowed_routes = ["login", "register", "static", "logout"]  
    if request.endpoint not in allowed_routes and "user" not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "error")
        return redirect("/login")

@app.before_request
def restrict_to_status():
    # Rutas permitidas sin autenticación
    allowed_routes = ["login", "static", "status", "logout", "register"]

    # Verificar si el usuario no está autenticado
    if "user" not in session and request.endpoint not in allowed_routes:
        flash("Debes iniciar sesión para acceder a esta página.", "error")
        return redirect("/login")

    # Verificar si el usuario está autenticado
    if "user" in session:
        user = Users.query.filter_by(username=session.get("user")).first()
        if user:
            # Si el usuario es un viewer, restringir acceso a otras rutas
            if user.role == "viewer" and request.endpoint not in ["status", "logout", "static"]:
                flash("No tienes permitido realizar esta accion.", "error")
                return redirect("/status")

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    session.pop("user", None)  # Eliminar la sesión del usuario
    print("Sesión cerrada correctamente.")  # Depuración
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect("/login")

# Ruta principal para mostrar las IPs
@app.route("/")
def index():
    ip_list = IP.query.all()
    active_count = IP.query.filter_by(status="activa").count()
    inactive_count = IP.query.filter_by(status="inactiva").count()

    # Obtener el rol del usuario actual
    user_role = None
    if "user" in session:
        user = Users.query.filter_by(username=session["user"]).first()
        if user:
            user_role = user.role

    return render_template(
        "index.html",
        ip_list=ip_list,
        active_count=active_count,
        inactive_count=inactive_count,
        user_role=user_role,
    )

# Ruta para mostrar las IPs activas y caídas
@app.route("/status")
@role_required(["viewer", "admin", "DM"])
def status():
    # Obtener parámetros de búsqueda y paginación desde la URL
    search_query = request.args.get("search", "").strip()
    page_active = request.args.get("page_active", 1, type=int)
    page_inactive = request.args.get("page_inactive", 1, type=int)
    per_page = request.args.get("per_page", 6, type=int)  # Valor predeterminado de 6 resultados por página

    # Consulta para IPs activas
    query_active = IP.query.filter_by(status="activa")
    if search_query:
        query_active = query_active.filter(
            (IP.name.ilike(f"%{search_query}%")) | (IP.address.ilike(f"%{search_query}%"))
        )
    pagination_active = query_active.paginate(page=page_active, per_page=per_page, error_out=False)

    # Consulta para IPs inactivas
    query_inactive = IP.query.filter_by(status="inactiva")
    if search_query:
        query_inactive = query_inactive.filter(
            (IP.name.ilike(f"%{search_query}%")) | (IP.address.ilike(f"%{search_query}%"))
        )
    pagination_inactive = query_inactive.paginate(page=page_inactive, per_page=per_page, error_out=False)

    return render_template(
        "status.html",
        pagination_active=pagination_active,
        pagination_inactive=pagination_inactive,
        active_ips=pagination_active.items,
        inactive_ips=pagination_inactive.items,
        search_query=search_query,
        per_page=per_page,
    )

# Ruta para agregar una nueva IP
@app.route("/add", methods=["POST"])
@role_required(["admin", "DM"])  # Seguro para que solo los roles autorizados puedan agregar IPs
def add_ip():
    ip_address = request.form.get("ip")
    ip_name = request.form.get("name")

    # Validar que los campos no estén vacíos
    if not ip_address or not ip_name:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(request.referrer)

    # Validar que la dirección IP sea válida
    import re
    ip_regex = re.compile(
        r"^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    )
    if not ip_regex.match(ip_address):
        flash("La dirección IP no es válida.", "error")
        return redirect(request.referrer)

    # validacion que hace que la dirección IP no esté duplicada en la base de datos
    existing_ip = IP.query.filter_by(address=ip_address).first()
    if existing_ip:
        flash("La dirección IP ya existe en la base de datos.", "error")
        return redirect(request.referrer)

    # Agrega la nueva IP a la base de datos
    try:
        new_ip = IP(address=ip_address, name=ip_name, status="activa")
        db.session.add(new_ip)
        db.session.commit()
        flash("IP agregada exitosamente.", "success")
    except Exception as e:
        flash(f"Error al agregar la IP: {str(e)}", "error")
        return redirect(request.referrer)

    # Redirigir a la página de estado de las IPs después de agregar
    return redirect("/status")

# Ruta para eliminar una IP + alerta agregada 
@app.route("/delete/<int:ip_id>")
@role_required(["admin", "DM"])
def delete_ip(ip_id):
    ip_entry = IP.query.get(ip_id)

    if ip_entry:
        # Enviar un correo indicando que la IP ha sido eliminada
        send_email(f"ALERTA: La IP {ip_entry.address} ({ip_entry.name}) ha sido eliminada.\nHora de eliminación: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # Eliminar la IP de la base de datos
        db.session.delete(ip_entry)
        db.session.commit()

    flash(f"La IP {ip_entry.address} ha sido eliminada exitosamente.", "success")
    return redirect("/")

# Ruta para editar una IP
@app.route("/edit/<int:ip_id>", methods=["POST"])
@role_required(["admin", "DM"])
def edit_ip(ip_id):
    new_address = request.form["new_ip"]
    new_name = request.form["new_name"]
    ip_entry = IP.query.get(ip_id)

    if ip_entry:
        old_address = ip_entry.address
        old_name = ip_entry.name

        # Actualizar los datos de la IP
        ip_entry.address = new_address
        ip_entry.name = new_name
        db.session.commit()

        # Enviar un correo indicando que la IP ha sido editada
        send_email(
            f"ALERTA: La IP {old_address} ({old_name}) ha sido editada.\n"
            f"Nueva dirección IP: {new_address}\n"
            f"Nuevo nombre: {new_name}\n"
            f"Hora de edición: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )

    flash(f"La IP {new_address} ha sido actualizada exitosamente.", "success")
    return redirect("/")

# Ruta para la página de administración
@app.route("/admin")
@role_required(["admin", "DM"])  # Decorador asegura que solo admin y DM accedan
def admin():
    users = Users.query.all()  # Obtener todos los usuarios de la base de datos
    return render_template("admin.html", users=users)

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@role_required(["DM", "admin"])  # Permitir acceso a DM y admin, pero restringir acciones
def edit_user(user_id):
    current_user = Users.query.filter_by(username=session.get("user")).first()
    if current_user.role == "admin":
        flash("No tienes permiso para editar usuarios.", "error")
        return redirect("/admin")

    user_to_edit = Users.query.get(user_id)
    if not user_to_edit:
        flash("El usuario no existe.", "error")
        return redirect("/admin")

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        role = request.form.get("role", "viewer")
        valid_roles = ["viewer", "admin", "DM"]

        if role not in valid_roles:
            flash("Rol no válido.", "error")
            return redirect(request.referrer)

        # Verificar si el nombre de usuario o correo ya existen
        existing_user = Users.query.filter(Users.username == username, Users.id != user_id).first()
        existing_email = Users.query.filter(Users.email == email, Users.id != user_id).first()
        if existing_user:
            flash("El nombre de usuario ya está en uso.", "error")
            return redirect(request.referrer)
        if existing_email:
            flash("El correo electrónico ya está en uso.", "error")
            return redirect(request.referrer)

        # Actualizar los datos del usuario
        user_to_edit.username = username
        user_to_edit.email = email
        user_to_edit.role = role
        db.session.commit()

        flash("Usuario actualizado exitosamente.", "success")
        return redirect("/admin")

    return render_template("edit_user.html", user=user_to_edit)

@app.route("/approve_users", methods=["GET", "POST"])
@role_required(["admin", "DM"])  # Solo admin y DM pueden acceder a esta ruta
def approve_users():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        user_to_approve = Users.query.get(user_id)

        if not user_to_approve:
            flash("El usuario no existe.", "error")
            return redirect("/approve_users")

        # Verificar si el usuario a aprobar es un DM
        if user_to_approve.role == "DM":
            current_user = Users.query.filter_by(username=session.get("user")).first()
            if current_user.role != "DM":
                flash("Solo un DM puede aprobar a otro DM.", "error")
                return redirect("/approve_users")

        # Aprobar al usuario
        user_to_approve.approved = True
        db.session.commit()
        flash(f"El usuario {user_to_approve.username} ha sido aprobado.", "success")
        return redirect("/approve_users")

    # Manejar solicitudes GET para mostrar usuarios pendientes
    pending_users = Users.query.filter_by(approved=False).all()
    return render_template("approve_users.html", pending_users=pending_users)

@app.route("/api/pending_users_count")
def pending_users_count():
    count = Users.query.filter_by(approved=False).count()
    return jsonify({"count": count})

@app.route("/delete_user/<int:user_id>", methods=["POST"])
@role_required(["DM", "admin"])  # Permitir acceso a DM y admin, pero restringir acciones
def delete_user(user_id):
    current_user = Users.query.filter_by(username=session.get("user")).first()
    if current_user.role == "admin":
        flash("No tienes permiso para eliminar usuarios.", "error")
        return redirect("/admin")

    user_to_delete = Users.query.get(user_id)
    if not user_to_delete:
        flash("El usuario no existe.", "error")
        return redirect("/admin")

    # Eliminar al usuario
    db.session.delete(user_to_delete)
    db.session.commit()

    flash(f"El usuario {user_to_delete.username} ha sido eliminado exitosamente.", "success")
    return redirect("/admin")

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_users = Users.query.count()
    total_ips = IP.query.count()
    return jsonify({"total_users": total_users, "total_ips": total_ips})

@app.route("/reject_user", methods=["POST"])
@role_required(["admin", "DM"])  # Solo roles autorizados pueden rechazar usuarios
def reject_user():
    user_id = request.form.get("user_id")

    # Buscar al usuario en la base de datos
    user = Users.query.get(user_id)
    if not user:
        flash("El usuario no existe.", "error")
        return redirect("/approve_users")

    # Eliminar al usuario de la base de datos
    db.session.delete(user)
    db.session.commit()

    flash(f"El usuario {user.username} ha sido rechazado y eliminado.", "success")
    return redirect("/approve_users")

# Iniciar el monitoreo en un hilo separado
print("Iniciando el hilo de monitoreo...")  # Depuración
threading.Thread(target=monitor_ips, daemon=True).start()

if __name__ == "__main__":
    print("Iniciando el hilo de monitoreo...")  # Depuración
    threading.Thread(target=monitor_ips, daemon=True).start()
    app.run(debug=True)

@app.route("/add_ip", methods=["POST"])
@role_required(["admin", "DM"])  # Se asegura de que solo roles autorizados puedan agregar IPs
def add_ip():
    ip_address = request.form.get("ip_address")
    ip_name = request.form.get("ip_name")

    # Verifica que los campos no estén vacíos
    if not ip_address or not ip_name:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(request.referrer)

    # Agrega la nueva IP a la base de datos
    new_ip = IP(address=ip_address, name=ip_name, status="activa")
    db.session.add(new_ip)
    db.session.commit()

    flash("IP agregada exitosamente.", "success")
    return redirect("/status")


