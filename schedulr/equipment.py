# Description: This file contains the equipment blueprint for the Schedulr application.
# Resources: https://nickgeorge.net/programming/python-sqlite3-extract-to-dictionary/

from flask import Blueprint, request, jsonify, Response

from schedulr.auth import login_required
from schedulr.db import get_db

from sqlite3 import Row, Connection, IntegrityError, Error, Cursor

bp = Blueprint(name='equipment', import_name=__name__, url_prefix='/equipment')


@bp.route(rule='/', methods=(['GET']))
def index():
    db = get_db()

    # Select all equipment from the database, returns as a list of SQlite Row objects.
    equipment_rows: list[Row] = db.execute(
        'SELECT * FROM equipment').fetchall()

    # Convert the list of SQlite Row objects to a list of dictionaries, which can be serialized to JSON.
    return [dict(row) for row in equipment_rows]


@bp.route(rule='/', methods=(['POST']))
def create_equipment():
    name = request.form['name']
    description = request.form['description']

    if not name or not description:
        return {'error': 'A name and description are required.'}, 400

    db: Connection = get_db()
    db.execute(
        'INSERT INTO equipment (name, description) VALUES (?, ?)', (name, description))
    db.commit()
    return {'message': 'Equipment successfully created.'}, 201


@bp.route(rule='/<int:id>', methods=(['GET']))
def get_equipment(id: int):
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
        return {'error': f'Equipment with id {id} does not exist.'}, 404
    # Return the database row as a dictionary to be serialized to JSON.
    return dict(equipment)


@bp.route(rule='/<int:id>', methods=(['DELETE']))
def delete_equipment(id):
    db = get_db()
    cursor: Cursor = db.execute('DELETE FROM equipment WHERE id = ?', (id,))
    db.commit()
    # rowcount returns the number of rows that were modified by the DELETE statement.
    num_rows_deleted = cursor.rowcount
    # If no rows were deleted, the equipment with the specified id does not exist.
    if num_rows_deleted == 0:
        return {'error': f'Equipment with id {id} does not exist.'}, 404
    return {'message': f'Equipment with id {id} successfully deleted.'}, 200


@bp.route(rule='/<int:id>', methods=(['PUT']))
def update_equipment(id):

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
        return {'error': f'Equipment with id {id} does not exist.'}, 404
    return {'message': f'Equipment {id} successfully updated.'}


def check_if_equipment_exists(id):
    db = get_db()
    equipment = db.execute(
        'SELECT * FROM equipment WHERE id = ?', (id,)).fetchone()
    if equipment is None:
        return False
    return True
