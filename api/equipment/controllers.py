import logging
from flask import make_response, current_app
from sqlite3 import Row, Connection, DatabaseError
from api.db import get_db

####################################
## EQUIPMENT CONTROLLER FUNCTIONS ##
####################################

def get_equipment_list():
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
        current_app.logger.error(msg='Database error occurred.')
        return make_response({'status': 'error', 'message': e.args[0]}, 500)




