from flask import Blueprint, render_template, abort
from app.models import Trabajo

cliente_bp = Blueprint('cliente', __name__)

# Nota que aquí usamos <uuid_publico> en vez de un ID normal
@cliente_bp.route('/presupuesto/<uuid_publico>')
def ver_presupuesto(uuid_publico):
    # Buscamos el trabajo por su UUID seguro. Si no existe, da error 404
    trabajo = Trabajo.query.filter_by(uuid_publico=uuid_publico).first_or_404()
    
    # Esta vista NO TIENE @login_required, cualquiera con el link puede verla
    return render_template('cliente/presupuesto_publico.html', trabajo=trabajo)