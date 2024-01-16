from flask import Blueprint, request, abort, Request
from sqlite3 import Row, Connection, DatabaseError, Cursor
from schedulr.db import get_db
from schedulr.auth import login_required


bp = Blueprint(name='reservations', import_name=__name__,
               url_prefix='/reservations')

########################################
# REQUEST METHOD DISPATCHER FUNCTIONS ##
########################################


@bp.route(rule='/', methods=(['GET']))
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

        # Select all reservations from the database, returns as a list of SQlite Row objects.
        query = """SELECT user.username as user, equipment.name as equipment, time_slot.start_time as timeslot FROM reservation
                JOIN user ON reservation.user_id = user.id
                JOIN equipment ON reservation.equipment_id = equipment.id
                JOIN time_slot ON reservation.time_slot_id = time_slot.id"""

        reservation_rows: list[Row] = db.execute(query).fetchall()

        # Convert the list of SQlite Row objects to a list of dictionaries, which can be serialized to JSON.
        return [dict(row) for row in reservation_rows]
    except DatabaseError as e:
        return {'error': e.args[0]}, 500


@bp.route(rule='/', methods=(['POST']))
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
    data = request.get_json()
    user_id = request.get_json().get('user_id')
    equipment_id = request.get_json().get('equipment_id')
    time_slot_id = request.get_json().get('time_slot_id')

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
        return dict(reservation_row)
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
