from flask import request, render_template, redirect, url_for, flash
from api.auth.decorators import login_required, admin_required
from . import equipment
from .controllers import get_equipment_list, get_equipment_details, create_equipment, update_equipment, delete_equipment

##############################
## EQUIPMENT VIEW FUNCTIONS ##
##############################


@equipment.get('/')
def index():
    e = get_equipment_list()
    return render_template('equipment/index.html', equipment=e)


@equipment.get('/<int:id>')
def detail(id):
    e = get_equipment_details(id)
    return render_template('equipment/detail.html', equipment=e)


@equipment.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        e = create_equipment(request)
        if e is None:
            return render_template('equipment/create.html')
        flash('Equipment created successfully!')
        return redirect(url_for('equipment.index'))
    return render_template('equipment/create.html')


@equipment.put('/<int:id>')
@login_required
def update(id: int):
    e = update_equipment(id=id, request=request)
    if e is None:
        return render_template('equipment/update.html')
    flash('Equipment updated successfully!')
    return redirect(url_for('equipment.index'))


@equipment.delete('/<int:id>')
@login_required
def delete(id: int):
    delete_equipment(id)
    flash('Equipment deleted successfully!')
    return redirect(url_for('equipment.index'))
