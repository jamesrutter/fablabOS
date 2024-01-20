from sqlite3 import Row, DatabaseError
from api.db import get_db

###############################
######## TIME SLOTS ###########
###############################


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
