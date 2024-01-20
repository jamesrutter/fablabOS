from flask import Blueprint, request
from sqlite3 import Row, DatabaseError, Cursor
from api.db import get_db
from api.auth import login_required
from werkzeug.exceptions import BadRequestKeyError

from .validators import validate_reservation
from api.auth import owner_required

from api.mail import confirmation_email


def create_reservation_bp():
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
            return {'status': 'success', 'data': [dict(row) for row in reservation_rows]}, 200
        except DatabaseError as e:
            return {'status': 'error', 'message': e.args[0]}, 500

    @bp.post(rule='/')
    @login_required
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
            return {'status': 'fail', 'hint': f'{e.description} Check the following parameter: {e.args[0]}'}, 400

        (is_valid, message) = validate_reservation(
            user_id=user_id, equipment_id=equipment_id, time_slot_id=time_slot_id)
        if not is_valid:
            return {'status': 'error', 'message': message}, 400
        db = get_db()
        try:
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
            # Example usage
            confirmation_email(
                user_email="jamesdavidrutter@gmail.com",
                user_name="James",
                reservation_details="Date: April 5, 2024\nTime: 10:00 AM - 12:00 PM\nEquipment: 3D Printer"
            )
            return {'status': 'Success', 'data': reservation_data}, 201
        except DatabaseError as e:
            db.rollback
            return {'status': e.args[0]}, 500

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
        db = get_db()
        try:
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
            reservation: Row = db.execute(query, (id,)).fetchone()

            if reservation is None:
                return {'status': 'error', 'message': 'Reservation not found.'}, 404

            # Convert the SQlite Row object to a dictionary, which can be serialized to JSON.
            data = dict(reservation)
            return {'status': 'success', 'data': data}, 200
        except DatabaseError as e:
            return {'status': 'error', 'message': e.args[0]}, 500
        finally:
            db.close()

    @bp.put(rule='/<int:id>')
    @login_required
    @owner_required
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
        db = get_db()
        try:
            # Update the reservation in the database.
            query = """UPDATE reservation SET user_id = ?, equipment_id = ?, time_slot_id = ? WHERE id = ?"""
            db.execute(query, (request.form['user_id'], request.form['equipment_id'],
                               request.form['time_slot_id'], id))
            db.commit()

            # Select the reservation from the database, returns as a SQlite Row object.
            query = """SELECT * FROM reservation WHERE id = ?"""
            reservation: Row = db.execute(query, (id,)).fetchone()

            # Convert the SQlite Row object to a dictionary, which can be serialized to JSON.
            data = dict(reservation)
            return {'status': 'success', 'data': data}, 200
        except DatabaseError as e:
            db.rollback()
            return {'status': 'error', 'message': e.args[0]}, 500
        finally:
            db.close()

    @bp.delete(rule='/<int:id>')
    @login_required
    @owner_required
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
        db = get_db()
        try:
            # Delete the reservation from the database.
            query = """DELETE FROM reservation WHERE id = ?"""
            db.execute(query, (id,))
            db.commit()
            return {'status': 'success', 'data': None}, 200
        except DatabaseError as e:
            db.rollback()
            return {'status': 'error', 'message': e.args[0]}, 500
        finally:
            db.close()

    # Now register the sub-module routes with the blueprint
    from .timeslots import get_timeslots
    bp.get('/timeslots')(get_timeslots)

    return bp


reservations_bp = create_reservation_bp()
