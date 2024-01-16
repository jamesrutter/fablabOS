from flask import Blueprint, request, abort
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
        query = """SELECT user.username as user, equipment.name as equipment, timeslot.start_time as timeslot FROM reservation
                JOIN user ON reservation.user_id = user.id
                JOIN equipment ON reservation.equipment_id = equipment.id
                JOIN timeslot ON reservation.timeslot_id = timeslot.id"""

        reservation_rows: list[Row] = db.execute(query).fetchall()

        # Convert the list of SQlite Row objects to a list of dictionaries, which can be serialized to JSON.
        return [dict(row) for row in reservation_rows]
    except DatabaseError as e:
        return {'error': e.args[0]}, 500
