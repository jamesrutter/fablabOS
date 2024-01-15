# Description: This file contains the equipment blueprint for the Schedulr application.
# Resources: https://nickgeorge.net/programming/python-sqlite3-extract-to-dictionary/

from flask import (
    Blueprint, flash, g, request, jsonify
)

from schedulr.auth import login_required
from schedulr.db import get_db

from sqlite3 import Row

bp = Blueprint(name='equipment', import_name=__name__, url_prefix='/equipment')


@bp.route(rule='/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name or not description:
            return {'error': 'A name and description are required.'}, 400

        else:
            db = get_db()
            db.execute(
                'INSERT INTO equipment (name, description) VALUES (?, ?)', (name, description))
            db.commit()
            return {'message': 'Equipment successfully created.'}, 201
    if request.method == 'GET':

        db = get_db()

        # Select all equipment from the database, returns as a list of SQlite Row objects.
        equipment_rows: list[Row] = db.execute(
            'SELECT * FROM equipment').fetchall()

        # Convert the list of SQlite Row objects to a list of dictionaries, which can be serialized to JSON.
        return [dict(row) for row in equipment_rows]
    return {'error': 'Invalid request method.', 'status': 400}


@bp.route(rule='/<int:id>', methods=('GET', 'PUT', 'DELETE'))
def equipment(id):
    if request.method == 'GET':
        db = get_db()
        equipment: Row = db.execute(
            'SELECT * FROM equipment WHERE id = ?', (id,)).fetchone()
        if equipment is None:
            return {'error': f'Equipment with id {id} does not exist.'}
        # Return the database row as a dictionary to be serialized to JSON.
        return dict(equipment)

    elif request.method == 'DELETE':
        db = get_db()
        db.execute('DELETE FROM equipment WHERE id = ?', (id,))
        db.commit()
        return {'message': f'Equipment with id {id} successfully deleted.'}

    elif request.method == 'PUT':
        name = request.form['name']
        description = request.form['description']

        if not name or not description:
            return {'error': 'A name and description are required.'}

        else:
            db = get_db()
            db.execute(
                'UPDATE equipment SET name = ?, description = ? WHERE id = ?', (name, description, id))
            db.commit()
            return {'message': f'Equipment {id} successfully updated.'}

    return {'error': 'Invalid request method.'}
