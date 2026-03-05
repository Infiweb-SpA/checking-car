import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import Trabajo
from app import db

taller_bp = Blueprint('taller', __name__)

@taller_bp.route('/dashboard')
@login_required
def dashboard():
    # ⚠️ RECUERDA: Pon tu URL actual de DevTunnels aquí
    base_url = "https://jl2flq77-5000.brs.devtunnels.ms" 
    
    busqueda = request.args.get('q')
    filtro_estado = request.args.get('estado')
    
    # Inicia la consulta filtrando solo los trabajos del mecánico logueado
    query = Trabajo.query.filter_by(taller_id=current_user.id)
    
    if busqueda:
        query = query.filter(Trabajo.patente.ilike(f'%{busqueda}%'))
        
    if filtro_estado:
        query = query.filter(Trabajo.estado == filtro_estado)
        
    # Ordenar por fecha y limitar a 50 resultados para que no cargue lento
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

        # --- LÓGICA DE LAS IMÁGENES (MÚLTIPLES) ---
        imagenes_files = request.files.getlist('imagenes')
        nombres_guardados = []
        
        for img in imagenes_files:
            if img and img.filename != '':
                # Genera un nombre seguro y único
                extension = img.filename.rsplit('.', 1)[1].lower()
                nombre_imagen = f"{uuid.uuid4().hex}.{extension}"
                
                # Crea la ruta si no existe
                upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                
                # Guarda la foto en la carpeta
                img.save(os.path.join(upload_path, nombre_imagen))
                nombres_guardados.append(nombre_imagen)

        # Junta todos los nombres de las fotos separadas por comas
        texto_imagenes_db = ",".join(nombres_guardados) if nombres_guardados else None

        # --- GUARDAR EN BASE DE DATOS ---
        nuevo = Trabajo(
            patente=patente.upper(),
            nombre_cliente=nombre_cliente.title() if nombre_cliente else "Cliente Sin Nombre",
            tipo_vehiculo=tipo_vehiculo,
            marca_vehiculo=marca_vehiculo.title() if marca_vehiculo else "Sin Marca",
            telefono_cliente=telefono,
            descripcion=descripcion,
            total_costo=int(costo),
            imagen_evidencia=texto_imagenes_db, # Guardamos el string largo aquí
            taller_id=current_user.id
        )
        
        db.session.add(nuevo)
        db.session.commit()
        
        return redirect(url_for('taller.dashboard'))

    return render_template('taller/nuevo.html')

@taller_bp.route('/marcar_pagado/<int:id>', methods=['POST'])
@login_required
def marcar_pagado(id):
    trabajo = Trabajo.query.get_or_404(id)
    
    # Verifica que el mecánico que aprieta el botón sea el dueño de este registro
    if trabajo.taller_id == current_user.id:
        trabajo.estado = "Pagado"
        trabajo.monto_pagado = trabajo.total_costo
        db.session.commit()
        
    return redirect(url_for('taller.dashboard'))

# Pega esto al final de app/taller/routes.py

@taller_bp.route('/editar_trabajo/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_trabajo(id):
    # Buscamos el trabajo. Si no existe da error 404.
    trabajo = Trabajo.query.get_or_404(id)
    
    # Seguridad: Evitamos que un mecánico edite el auto de otro taller
    if trabajo.taller_id != current_user.id:
        return redirect(url_for('taller.dashboard'))

    if request.method == 'POST':
        # Capturamos los nuevos datos y los reemplazamos
        trabajo.patente = request.form.get('patente').upper()
        trabajo.nombre_cliente = request.form.get('nombre_cliente').title()
        trabajo.tipo_vehiculo = request.form.get('tipo_vehiculo')
        trabajo.marca_vehiculo = request.form.get('marca_vehiculo').title()
        trabajo.telefono_cliente = request.form.get('telefono')
        trabajo.descripcion = request.form.get('descripcion')
        trabajo.total_costo = int(request.form.get('costo'))
        
        # Guardamos los cambios
        db.session.commit()
        return redirect(url_for('taller.dashboard'))

    # Si es GET, le mostramos el formulario con los datos actuales
    return render_template('taller/editar.html', trabajo=trabajo)    