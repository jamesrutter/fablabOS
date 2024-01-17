from datetime import datetime
from flask import Blueprint, request, abort, Request
from sqlite3 import Row, Connection, DatabaseError, Cursor
from schedulr.db import get_db
from schedulr.auth import login_required
from werkzeug.exceptions import BadRequestKeyError


bp = Blueprint(name='reservations', import_name=__name__,
               url_prefix='/reservations')

########################################
# REQUEST METHOD DISPATCHER FUNCTIONS ##
########################################


@bp.get(rule='/')
def index():
    """
    Retrieve a list of all reservations from the database.

    This endpoint fetches all reservation records from the database and returns them 
    as a list of JSON objects. Each object represents a reservation with all its details.

    Returns:
        Response: A JSON list of all reservations. Each reservation is a dictionary 
        containing reservation details. If no reservations are found, an empty list is returned.
    """
    try:
        db = get_db()

        # Select all reservations and their details from the database, returns as a list of SQlite Row objects.
        query = """
        SELECT 
            reservation.id AS reservation_id,
            user.username,
            user.role,
            equipment.name AS equipment_name,
            equipment.description AS equipment_description,
            time_slot.start_time,
            time_slot.end_time
        FROM 
            reservation
        JOIN 
            user ON reservation.user_id = user.id
        JOIN 
            equipment ON reservation.equipment_id = equipment.id
        JOIN 
            time_slot ON reservation.time_slot_id = time_slot.id;
        """

        reservation_rows: list[Row] = db.execute(query).fetchall()

        # Convert the list of SQlite Row objects to a list of dictionaries, which can be serialized to JSON.
        return [dict(row) for row in reservation_rows]
    except DatabaseError as e:
        return {'error': e.args[0]}, 500


@bp.post(rule='/')
def make_reservation():
    """
    Make a reservation for a piece of equipment.

    This endpoint creates a new reservation record in the database. 
    The reservation is created for a specific user, equipment and timeslot.

    Args:
        user_id (int): The ID of the user making the reservation.
        equipment_id (int): The ID of the equipment being reserved.
        time_slot_id (int): The ID of the timeslot being reserved.

    Returns:
        Response: A JSON object representing the reservation that was created. 
        If the reservation could not be created, an error message with a 500 status code is returned.
    """
    try:
        user_id = request.form['user_id']
        equipment_id = request.form['equipment_id']
        time_slot_id = request.form['time_slot_id']
    except BadRequestKeyError as e:
        return {'error': f'{e.description}', 'hint': f'Check the following parameter: {e.args[0]}'}, 400

    if not user_id or not equipment_id or not time_slot_id:
        return {'error': 'A user ID, equipment ID and timeslot ID are required.'}, 400

    if not check_if_resource_exists(resource_name='user', id=int(user_id)):
        return {'error': 'User not found.'}, 404
    if not check_if_resource_exists(resource_name='equipment', id=int(equipment_id)):
        return {'error': 'Equipment not found.'}, 404
    if not check_if_resource_exists(resource_name='time_slot', id=int(time_slot_id)):
        return {'error': 'Timeslot not found.'}, 404

    if not check_if_resource_available(resource_name='equipment', id=int(equipment_id), time_slot_id=int(time_slot_id)):
        return {'error': 'Equipment is not available for this timeslot.'}, 400
    if not check_if_resource_available(resource_name='user', id=int(user_id), time_slot_id=int(time_slot_id)):
        return {'error': 'User already has a reservation for this timeslot.'}, 400

    try:
        db = get_db()

        # Insert the reservation into the database.
        query = """INSERT INTO reservation (user_id, equipment_id, time_slot_id) VALUES (?, ?, ?)"""
        db.execute(query, (user_id, equipment_id, time_slot_id))
        db.commit()

        # Select the reservation from the database, returns as a SQlite Row object.
        query = """SELECT * FROM reservation WHERE user_id = ? AND equipment_id = ? AND time_slot_id = ?"""
        reservation_row: Cursor = db.execute(
            query, (user_id, equipment_id, time_slot_id)).fetchone()

        # Convert the SQlite Row object to a dictionary, which can be serialized to JSON.
        reservation_data = dict(reservation_row)
        return {'message': 'Reservation successfully created.', 'reservation': reservation_data}, 201
    except DatabaseError as e:
        return {'error': e.args[0]}, 500


@bp.get(rule='/<int:id>')
def get_reservation(id):
    """
    Retrieve a reservation from the database.

    This endpoint fetches a reservation record from the database and returns it 
    as a JSON object. The object represents a reservation with all its details.

    Args:
        id (int): The ID of the reservation to retrieve.

    Returns:
        Response: A JSON object representing the reservation that was retrieved. 
        If the reservation could not be retrieved, an error message with a 500 status code is returned.
    """
    try:
        db = get_db()

        # Select the reservation from the database, returns as a SQlite Row object.
        query = """
        SELECT 
            reservation.id AS reservation_id,
            user.username,
            user.role,
            equipment.name AS equipment_name,
            equipment.description AS equipment_description,
            time_slot.start_time,
            time_slot.end_time
        FROM 
            reservation
        JOIN 
            user ON reservation.user_id = user.id
        JOIN 
            equipment ON reservation.equipment_id = equipment.id
        JOIN 
            time_slot ON reservation.time_slot_id = time_slot.id
        WHERE
            reservation.id = ?;
        """
        reservation_row: Cursor = db.execute(query, (id,)).fetchone()

        if reservation_row is None:
            return {'error': 'Reservation not found.'}, 404

        # Convert the SQlite Row object to a dictionary, which can be serialized to JSON.
        reservation_data = dict(reservation_row)
        return reservation_data, 200
    except DatabaseError as e:
        return {'error': e.args[0]}, 500


@bp.put(rule='/<int:id>')
def update_reservation(id):
    """
    Update a reservation in the database.

    This endpoint updates a reservation record in the database.

    Args:
        id (int): The ID of the reservation to update.

    Returns:
        Response: A JSON object representing the reservation that was updated. 
        If the reservation could not be updated, an error message with a 500 status code is returned.
    """
    try:
        db = get_db()

        # Update the reservation in the database.
        query = """UPDATE reservation SET user_id = ?, equipment_id = ?, time_slot_id = ? WHERE id = ?"""
        db.execute(query, (request.form['user_id'], request.form['equipment_id'],
                           request.form['time_slot_id'], id))
        db.commit()

        # Select the reservation from the database, returns as a SQlite Row object.
        query = """SELECT * FROM reservation WHERE id = ?"""
        reservation_row: Cursor = db.execute(query, (id,)).fetchone()

        # Convert the SQlite Row object to a dictionary, which can be serialized to JSON.
        reservation_data = dict(reservation_row)
        return {'message': 'Reservation successfully updated.', 'reservation': reservation_data}, 200
    except DatabaseError as e:
        return {'error': e.args[0]}, 500


@bp.delete(rule='/<int:id>')
def delete_reservation(id):
    """
    Delete a reservation from the database.

    This endpoint deletes a reservation record from the database.

    Args:
        id (int): The ID of the reservation to delete.

    Returns:
        Response: A success message if the reservation is deleted successfully, 
        or an error message with a 500 status code if the reservation could not be deleted.
    """
    try:
        db = get_db()

        # Delete the reservation from the database.
        query = """DELETE FROM reservation WHERE id = ?"""
        db.execute(query, (id,))
        db.commit()

        return {'message': 'Reservation successfully deleted.'}
    except DatabaseError as e:
        return {'error': e.args[0]}, 500


###############################
######## TIME SLOTS ###########
###############################


@bp.route(rule='/timeslots', methods=(['GET']))
def get_timeslots():
    """
    Retrieve a list of all available timeslots.

    This endpoint fetches all timeslot records from the database and returns them 
    as a list of JSON objects. Each object represents a timeslot with all its details.

    Returns:
        Response: A JSON list of all timeslots. Each timeslot is a dictionary 
        containing timeslot details. If no timeslots are found, an empty list is returned.
    """
    try:
        db = get_db()

        # Select all timeslots from the database, returns as a list of SQlite Row objects.
        query = """SELECT * FROM time_slot"""

        timeslot_rows: list[Row] = db.execute(query).fetchall()

        # Convert the list of SQlite Row objects to a list of dictionaries, which can be serialized to JSON.
        return [dict(row) for row in timeslot_rows]
    except DatabaseError as e:
        return {'error': e.args[0]}, 500


#############################################################
###################### HELPER FUNCTIONS #####################
#############################################################


def check_if_resource_exists(resource_name: str, id: int) -> bool:
    """This utility function checks if a resource exists in the database.

    Args:
        resource_name (str): The name of the resource to check.
        id (int): The ID of the resource to check.

    Returns:
        bool: True if the resource exists, False otherwise.
    """
    db = get_db()
    resource = db.execute(
        f'SELECT * FROM {resource_name} WHERE id = ?', (id,)).fetchone()
    if resource is None:
        return False
    return True


def check_if_resource_available(resource_name: str, id: int, time_slot_id: int) -> bool:
    """This utility function checks if a resource is available for a given timeslot.

    Args:
        resource_name (str): The name of the resource to check.
        id (int): The ID of the resource to check.
        time_slot_id (int): The ID of the timeslot to check.

    Returns:
        bool: True if the resource is available for the timeslot, False otherwise.
    """
    db = get_db()
    resource = db.execute(
        f'SELECT * FROM reservation WHERE {resource_name}_id = ? AND time_slot_id = ?', (id, time_slot_id)).fetchone()
    if resource is None:
        return True
    return False


def validate_form_fields(*fields):
    missing_fields = [field for field in fields if not request.form.get(field)]
    if missing_fields:
        error = False, f"Missing fields: {', '.join(missing_fields)}"
        return error, 400
    pass
