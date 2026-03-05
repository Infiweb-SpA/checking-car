import uuid
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Para cargar el usuario en Flask-Login
@login_manager.user_loader
def load_user(id):
    return Taller.query.get(int(id))

class Taller(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_taller = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    
    # Relación: Un taller tiene muchos trabajos
    trabajos = db.relationship('Trabajo', backref='taller', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Trabajo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid_publico = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    
    patente = db.Column(db.String(10), nullable=False)
    # 👇 NUEVOS CAMPOS 👇
    nombre_cliente = db.Column(db.String(100), nullable=False)
    tipo_vehiculo = db.Column(db.String(50), nullable=False)
    marca_vehiculo = db.Column(db.String(50), nullable=False)
    imagen_evidencia = db.Column(db.Text, nullable=True) # Ahora es Text para aguantar muchas fotos
    # 👆 FIN NUEVOS CAMPOS 👆
    
    telefono_cliente = db.Column(db.String(20), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    total_costo = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default="Pendiente")
    monto_pagado = db.Column(db.Integer, default=0)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    taller_id = db.Column(db.Integer, db.ForeignKey('taller.id'), nullable=False)