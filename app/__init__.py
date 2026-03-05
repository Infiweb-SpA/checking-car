from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicializamos las extensiones sin asociarlas a la app todavía
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Si no está logueado, lo manda aquí

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)

    # Registrar los Blueprints (Los módulos de tu app)
    from app.auth.routes import auth_bp
    from app.taller.routes import taller_bp
    from app.cliente.routes import cliente_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(taller_bp, url_prefix='/taller')
    app.register_blueprint(cliente_bp, url_prefix='/cliente') # Este es público

     # NUEVO: Arreglo del 404. Redirigir la raíz al login
    from flask import redirect, url_for
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app