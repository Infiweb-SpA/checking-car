import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Llave secreta para las sesiones y seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-super-secreta-para-desarrollo'
    # Base de datos SQLite (perfecta para empezar local)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False