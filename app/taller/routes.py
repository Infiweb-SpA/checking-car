from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Trabajo
from flask import request, redirect, url_for, flash # Asegúrate de importar esto arriba
from app import db # Asegúrate de importar la db
import os
import uuid
from flask import current_app 
from werkzeug.utils import secure_filename

taller_bp = Blueprint('taller', __name__)

@taller_bp.route('/dashboard')
@login_required
def dashboard():
    base_url = "https://jl2flq77-5000.brs.devtunnels.ms" 
    
    # Capturamos búsqueda y filtros
    busqueda = request.args.get('q')
    filtro_estado = request.args.get('estado') # Puede ser 'Pendiente' o 'Pagado'
    
    # Iniciamos la consulta base (Solo trabajos de este taller)
    query = Trabajo.query.filter_by(taller_id=current_user.id)
    
    # Si hay búsqueda por patente, filtramos
    if busqueda:
        query = query.filter(Trabajo.patente.ilike(f'%{busqueda}%'))
        
    # Si el mecánico hizo clic en un filtro de estado (Pendientes o Pagados)
    if filtro_estado:
        query = query.filter(Trabajo.estado == filtro_estado)
        
    # Ordenamos por fecha (más recientes primero)
    trabajos = query.order_by(Trabajo.fecha.desc()).limit(50).all()
                          
    return render_template('taller/dashboard.html', 
                           trabajos=trabajos, 
                           base_url=base_url, 
                           busqueda=busqueda,
                           filtro_estado=filtro_estado)



@taller_bp.route('/nuevo_trabajo', methods=['GET', 'POST'])
@login_required
def nuevo_trabajo():
    if request.method == 'POST':
        patente = request.form.get('patente')
        nombre_cliente = request.form.get('nombre_cliente')
        tipo_vehiculo = request.form.get('tipo_vehiculo')
        marca_vehiculo = request.form.get('marca_vehiculo')
        telefono = request.form.get('telefono')
        descripcion = request.form.get('descripcion')
        costo = request.form.get('costo')

        # --- LÓGICA DE LA IMAGEN ---
        imagen_file = request.files.get('imagen')
        nombre_imagen = None
        
        if imagen_file and imagen_file.filename != '':
            # 1. Creamos un nombre seguro y único
            extension = imagen_file.filename.rsplit('.', 1)[1].lower()
            nombre_imagen = f"{uuid.uuid4().hex}.{extension}"
            
            # 2. Definimos dónde se guarda (carpeta static/uploads)
            upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_path, exist_ok=True) # Crea la carpeta si no existe
            
            # 3. Guardamos la imagen en el disco duro
            imagen_file.save(os.path.join(upload_path, nombre_imagen))

        # --- GUARDAR EN BASE DE DATOS ---
        nuevo = Trabajo(
            patente=patente.upper(),
            nombre_cliente=nombre_cliente.title(),
            tipo_vehiculo=tipo_vehiculo,
            marca_vehiculo=marca_vehiculo.title(),
            telefono_cliente=telefono,
            descripcion=descripcion,
            total_costo=int(costo),
            imagen_evidencia=nombre_imagen, # Guardamos solo el nombre del archivo
            taller_id=current_user.id
        )
        
        db.session.add(nuevo)
        db.session.commit()
        
        return redirect(url_for('taller.dashboard'))

    return render_template('taller/nuevo.html')

# Agrégalo al final de app/taller/routes.py

@taller_bp.route('/marcar_pagado/<int:id>', methods=['POST'])
@login_required
def marcar_pagado(id):
    # Buscamos el trabajo en la base de datos
    trabajo = Trabajo.query.get_or_404(id)
    
    # Por seguridad, verificamos que este trabajo sea de ESTE mecánico
    if trabajo.taller_id == current_user.id:
        trabajo.estado = "Pagado"
        trabajo.monto_pagado = trabajo.total_costo # Asumimos que pagó todo
        db.session.commit()
        
    return redirect(url_for('taller.dashboard'))