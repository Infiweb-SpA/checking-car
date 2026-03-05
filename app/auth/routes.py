from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from app.models import Taller

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está logueado, lo mandamos directo al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('taller.dashboard'))
    
    # Si el usuario hizo clic en "Entrar" (Envió el formulario)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 1. Buscamos el correo en la base de datos
        taller = Taller.query.filter_by(email=email).first()
        
        # 2. Verificamos si existe el taller y si la clave coincide
        if taller and taller.check_password(password):
            # ¡Todo correcto! Iniciamos sesión
            login_user(taller)
            return redirect(url_for('taller.dashboard')) # <--- AQUÍ TE LLEVA AL DASHBOARD
        else:
            # Error de credenciales
            flash('Correo o contraseña incorrectos. Intenta de nuevo.', 'error')
            return redirect(url_for('auth.login'))
            
    # Si solo está visitando la página (GET)
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))