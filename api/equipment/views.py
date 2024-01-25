from flask import request, render_template
from api.auth.decorators import login_required, admin_required
from . import equipment
from .controllers import get_equipment_list

##############################
## EQUIPMENT VIEW FUNCTIONS ##
##############################


@equipment.get('/')
def index():
    equipment = get_equipment_list()
    return render_template('elist.html', equipment_list=equipment)


# @equipment.get('/<int:id>')
# def detail(id):
#     equipment_details = get_equipment_details(id)
#     return render_template('detail.html', equipment=equipment_details)


# @equipment.post('/')
# @login_required
# @admin_required
# def create():
#     return create_equipment(request)


# @equipment.put('/<int:id>')
# @login_required
# @admin_required
# def update(id: int):
#     return update_equipment(id=id, request=request)


# @equipment.delete('/<int:id>')
# @login_required
# @admin_required
# def delete(id: int):
#     return delete_equipment(id)
