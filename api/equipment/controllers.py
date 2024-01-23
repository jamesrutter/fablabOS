from flask import make_response, current_app, Response, Request
from sqlite3 import Connection, DatabaseError, Cursor
from api.db import get_db
from .models import Equipment, EquipmentForm

##############################
## EQUIPMENT CRUD FUNCTIONS ##
##############################


def get_equipment_list() -> Response:
    """
    Retrieve a list of all equipment items from the database.

    This endpoint fetches all equipment records from the database and returns them 
    as a list of JSON objects. Each object represents a piece of equipment with all its details.

    Returns:
        Response: A JSON list of all equipment items. Each item is a dictionary 
        containing equipment details. If no equipment is found, an empty list is returned.
    """
    try:
        equipment_list = Equipment.all().serialize()
        current_app.logger.debug(
            msg='EQUIPMENT >> Successfully retrieved equipment list.')
        return make_response({'status': 'success', 'data': equipment_list}, 200)
    except DatabaseError as e:
        current_app.logger.error(
            f'EQUIPMENT >> Database error occurred while retrieving equipment list: {e}')
        return make_response({'status': 'error', 'message': e.args[0]}, 500)


def get_equipment_detail(id: int) -> Response:
    """This function returns a JSON response containing the equipment with the specified id, otherwise a 404 error.
    Since the sqlite Row object is not JSON serializable, it is converted to a dictionary before being returned.
    Flask takes care of serializing the dictionary to JSON automatically if a serializable object is returned.

    Args:
        id (int): equipment_id to be returned.

    Returns:
        Response: A JSON response containing the equipment with the specified id, otherwise a 404 error.
    """
    try:
        equipment = Equipment.get(id)
        if equipment is None:
            current_app.logger.warning(
                f'EQUIPMENT >> Equipment with id {id} does not exist.')
            return make_response({'status': 'error', 'message': f'Equipment not found.'}, 404)
        current_app.logger.debug(
            f'EQUIPMENT >> Successfully retrieved details for equipment id {id}.')
        return make_response({'status': 'success', 'data': equipment.to_dict()}, 200)
    except DatabaseError as e:
        current_app.logger.error(
            f'EQUIPMENT >> Database error occurred while retrieving equipment details: {e}')
        return make_response({'status': 'error', 'message': e.args[0]}, 500)


def create_equipment(request) -> Response:
    """
    Create a new equipment item in the database.

    This endpoint accepts form data to create a new equipment item. The `name` and 
    `description` fields are required. If any of these fields are missing, 
    the request is rejected with a 400 Bad Request error.

    Args:
        name (str): The name of the equipment.
        description (str): The description of the equipment.

    Returns:
        Response: A success message if the equipment is created successfully, 
        or an error message with a 400 status code if required fields are missing.
    """
    equipment = EquipmentForm(data=request.form)
    if not equipment.validate():
        current_app.logger.warning(
            f'EQUIPMENT >> Invalid form data: {equipment.errors}')
        return make_response({'status': 'error', 'message': 'Invalid form data.'}, 400)
    try:
        # new_equipment:Equipment = equipment.populate_obj(Equipment)

        current_app.logger.info(
            f'EQUIPMENT >> Successfully created equipment with id {new_equipment.id}.')
        return make_response({'status': 'success', 'message': 'Equipment successfully created.'}, 201)
    except DatabaseError as e:
        current_app.logger.error(
            f'EQUIPMENT >> Database error occurred while creating equipment: {e}')
        return make_response({'status': 'error', 'message': e.args[0]}, 500)


def update_equipment(id: int, request: Request) -> Response:
    """
    Update an existing equipment item in the database by its ID.

    This endpoint updates the details of an existing equipment item specified by its ID. 
    It accepts form data for `name` and `description`. If the equipment with the given ID 
    does not exist, it returns a 404 Not Found error.

    Args:
        id (int): The ID of the equipment to update.
        name (str): The new name for the equipment.
        description (str): The new description for the equipment.

    Returns:
        Response: A success message if the update is successful, 
        or an error message with a 404 status code if the equipment does not exist.
    """

    equipment_form = EquipmentForm(data=request.form)
    if not equipment_form.validate():
        current_app.logger.warning(
            f'EQUIPMENT >> Invalid form data: {equipment_form.errors}')
        return make_response({'status': 'error', 'message': 'Invalid form data.'}, 400)
    equipment_to_update = Equipment.get(id)
    equipment_form.populate_obj(equipment_to_update)
    if equipment_to_update is None:
        current_app.logger.warning(
            f'EQUIPMENT >> Equipment with id {id} does not exist.')
        return make_response({'status': 'error', 'message': f'Equipment with id {id} does not exist.'}, 404)

    try:
        equipment_to_update.save()
        return make_response({'status': 'success', 'message': f'Equipment {id} successfully updated.'}, 200)
    except DatabaseError as e:
        current_app.logger.error(
            f'Database error occurred while updating equipment: {e}')
        return make_response({'status': 'error', 'message': e.args[0]}, 500)


def delete_equipment(id: int) -> Response:
    """
    Delete an equipment item from the database by its ID.

    This endpoint deletes the equipment item corresponding to the given ID. 
    If no item with the specified ID exists, it returns a 404 Not Found error.

    Args:
        id (int): The ID of the equipment to delete.

    Returns:
        Response: A success message if the equipment is deleted successfully, 
        or an error message with a 404 status code if the equipment does not exist.
    """
    try:
        db: Connection = get_db()
        cursor: Cursor = db.execute(
            'DELETE FROM equipment WHERE id = ?', (id,))
        db.commit()
        # rowcount returns the number of rows that were modified by the DELETE statement.
        num_rows_deleted = cursor.rowcount
        # If no rows were deleted, the equipment with the specified id does not exist.
        if num_rows_deleted == 0:
            current_app.logger.warning(
                f'Attempt to delete non-existent equipment with id {id}.')
            return make_response({'status': 'error', 'message': f'Equipment not found'}, 404)
        current_app.logger.info(f'Successfully deleted equipment id {id}.')
        return make_response({}, 204)
    except DatabaseError as e:
        current_app.logger.error(
            f'Database error occurred while deleting equipment: {e}')
        return make_response({'status': 'error', 'message': e.args[0]}, 500)
