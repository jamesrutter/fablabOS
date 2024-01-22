import logging
from flask import request
from sqlite3 import Row, Connection, DatabaseError, Cursor
from api.db import get_db
from api.auth.decorators import login_required, admin_required
from . import equipment

##############################
## EQUIPMENT VIEW FUNCTIONS ##
##############################


@equipment.get('/')
def index():
    """
    Retrieve a list of all equipment items from the database.

    This endpoint fetches all equipment records from the database and returns them 
    as a list of JSON objects. Each object represents a piece of equipment with all its details.

    Returns:
        Response: A JSON list of all equipment items. Each item is a dictionary 
        containing equipment details. If no equipment is found, an empty list is returned.
    """
    try:
        db = get_db()

        # Select all equipment from the database, returns as a list of SQlite Row objects.
        equipment_rows: list[Row] = db.execute(
            'SELECT * FROM equipment').fetchall()

        # Convert the list of SQlite Row objects to a list of dictionaries, which can be serialized to JSON.
        return {'status': 'success', 'data': [dict(row) for row in equipment_rows]}, 200
    except DatabaseError as e:
        logging.exception(msg='Database error occurred.')
        return {'status': 'error', 'message': e.args[0]}, 500


@equipment.get('/<int:id>')
def detail(id: int):
    """This function returns a JSON response containing the equipment with the specified id, otherwise a 404 error.
    Since the sqlite Row object is not JSON serializable, it is converted to a dictionary before being returned.
    Flask takes care of serializing the dictionary to JSON automatically if a serializable object is returned.

    Args:
        id (int): equipment_id to be returned.

    Returns:
        Response: A JSON response containing the equipment with the specified id, otherwise a 404 error.
    """
    db = get_db()
    equipment: Row = db.execute(
        'SELECT * FROM equipment WHERE id = ?', (id,)).fetchone()
    if equipment is None:
        return {'status': 'error', 'message': f'Equipment not found.'}, 404
    # Return the database row as a dictionary to be serialized to JSON.
    return {'status': 'success', 'data': dict(equipment)}, 200


@equipment.post('/')
@login_required
@admin_required
def create():
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
    name = request.form['name']
    description = request.form['description']

    if not name or not description:
        return {'status': 'error', 'message': 'A name and description are required.'}, 400

    db: Connection = get_db()
    db.execute(
        'INSERT INTO equipment (name, description) VALUES (?, ?)', (name, description))
    db.commit()
    return {'status': 'success', 'message': 'Equipment successfully created.'}, 201


@equipment.delete('/<int:id>')
@login_required
@admin_required
def delete(id):
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
    db = get_db()
    cursor: Cursor = db.execute(
        'DELETE FROM equipment WHERE id = ?', (id,))
    db.commit()
    # rowcount returns the number of rows that were modified by the DELETE statement.
    num_rows_deleted = cursor.rowcount
    # If no rows were deleted, the equipment with the specified id does not exist.
    if num_rows_deleted == 0:
        return {'status': 'error', 'message': f'Equipment with id {id} does not exist.'}, 404
    return {},204 


@equipment.put('/<int:id>')
@login_required
@admin_required
def update(id):
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
    name = request.form['name']
    description = request.form['description']

    if not name or not description:
        return {'error': 'A name and description are required.'}

    db = get_db()
    cursor: Cursor = db.execute(
        'UPDATE equipment SET name = ?, description = ? WHERE id = ?', (name, description, id))
    db.commit()
    # rowcount returns the number of rows that were modified by the UPDATE statement.
    num_rows_updated = cursor.rowcount
    # If no rows were updated, the equipment with the specified id does not exist.
    if num_rows_updated == 0:
        return {'status': 'error', 'message': f'Equipment with id {id} does not exist.'}, 404
    return {'status': 'success', 'message': f'Equipment {id} successfully updated.'}, 200
