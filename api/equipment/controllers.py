from flask import make_response, current_app, Response
from sqlite3 import Row, Connection, DatabaseError, Cursor
from api.db import get_db

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
        db: Connection = get_db()

        # Select all equipment from the database, returns as a list of SQlite Row objects.
        equipment_rows: list[Row] = db.execute(
            'SELECT * FROM equipment').fetchall()

        # Convert the list of SQlite Row objects to a list of dictionaries, which can be serialized to JSON.
        current_app.logger.debug(msg='Successfully retrieved equipment list.')
        return make_response({'status': 'success', 'data': [dict(row) for row in equipment_rows]}, 200)
    except DatabaseError as e:
        current_app.logger.error(
            f'Database error occurred while retrieving equipment list: {e}')
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
        db: Connection = get_db()
        equipment: Row = db.execute(
            'SELECT * FROM equipment WHERE id = ?', (id,)).fetchone()
        if equipment is None:
            current_app.logger.warning(
                f'Equipment with id {id} does not exist.')
            return make_response({'status': 'error', 'message': f'Equipment not found.'}, 404)
        current_app.logger.debug(
            f'Successfully retrieved details for equipment id {id}.')
        return make_response({'status': 'success', 'data': dict(equipment)}, 200)
    except DatabaseError as e:
        current_app.logger.error(
            f'Database error occurred while retrieving equipment details: {e}')
        return make_response({'status': 'error', 'message': e.args[0]}, 500)


def create_equipment(equipment: dict[str, str]) -> Response:
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
    name = equipment['name']
    description = equipment['description']

    if not name or not description:
        return make_response({'status': 'error', 'message': 'A name and description are required.'}, 400)
    try:
        db: Connection = get_db()
        db.execute(
            'INSERT INTO equipment (name, description) VALUES (?, ?)', (name, description))
        db.commit()
        return make_response({'status': 'success', 'message': 'Equipment successfully created.'}, 201)
    except DatabaseError as e:
        current_app.logger.error(
            f'Database error occurred while creating equipment: {e}')
        return make_response({'status': 'error', 'message': e.args[0]}, 500)


def update_equipment(id: int, equipment: dict[str, str]) -> Response:
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
    name = equipment['name']
    description = equipment['description']

    if not name or not description:
        return make_response({'status': 'error', 'message': 'A name and description are required.'}, 400)
    try:
        db = get_db()
        cursor: Cursor = db.execute(
            'UPDATE equipment SET name = ?, description = ? WHERE id = ?', (name, description, id))
        db.commit()
        # rowcount returns the number of rows that were modified by the UPDATE statement.
        num_rows_updated = cursor.rowcount
        # If no rows were updated, the equipment with the specified id does not exist.
        if num_rows_updated == 0:
            return make_response({'status': 'error', 'message': f'Equipment with id {id} does not exist.'}, 404)
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


#################################
## EQUIPMENT UTILITY FUNCTIONS ##
#################################


def check_if_equipment_exists(id: int):
    db = get_db()
    equipment = db.execute(
        'SELECT * FROM equipment WHERE id = ?', (id,)).fetchone()
    if equipment is None:
        return False
    return True
