from app import create_app, db
from app.models import Taller, Trabajo

app = create_app()

with app.app_context():
    # 1. Crear la base de datos por si no existe
    db.create_all()

    # 2. Revisar si ya existe el taller para no duplicarlo
    if not Taller.query.filter_by(email="maestro@taller.cl").first():
        
        # Crear un Mecánico Falso
        nuevo_taller = Taller(nombre_taller="Taller Los Pinos Araucanía", email="maestro@taller.cl")
        nuevo_taller.set_password("123456") # Contraseña fácil para probar
        db.session.add(nuevo_taller)
        db.session.commit()

        # Crear un Trabajo Falso asociado a ese mecánico (CON LOS DATOS NUEVOS)
        nuevo_trabajo = Trabajo(
            patente="AB-CD-12",
            nombre_cliente="Juan Pérez",         # <-- NUEVO CAMPO
            tipo_vehiculo="Camioneta",           # <-- NUEVO CAMPO
            marca_vehiculo="Toyota Hilux",       # <-- NUEVO CAMPO
            telefono_cliente="56920368688", 
            descripcion="Cambio de pastillas de freno y afinamiento completo.",
            total_costo=85000,
            estado="Pendiente",                  # Estado inicial de la deuda
            monto_pagado=0,                      # Aún no paga nada
            taller_id=nuevo_taller.id
        )
        db.session.add(nuevo_trabajo)
        db.session.commit()

        print("✅ ¡Datos creados exitosamente! Ya puedes iniciar sesión.")
    else:
        print("⚠️ Los datos ya existían en la base de datos.")