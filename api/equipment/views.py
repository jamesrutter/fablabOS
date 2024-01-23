from flask import request
from api.auth.decorators import login_required, admin_required
from . import equipment
from .controllers import get_equipment_list, get_equipment_detail, create_equipment, update_equipment, delete_equipment

##############################
## EQUIPMENT VIEW FUNCTIONS ##
##############################


@equipment.get('/')
def index():
    return get_equipment_list()


@equipment.get('/<int:id>')
def detail(id):
    return get_equipment_detail(id)


@equipment.post('/')
@login_required
@admin_required
def create():
    return create_equipment(request)


@equipment.put('/<int:id>')
@login_required
@admin_required
def update(id: int):
    return update_equipment(id=id, request=request)


@equipment.delete('/<int:id>')
@login_required
@admin_required
def delete(id: int):
    return delete_equipment(id)
