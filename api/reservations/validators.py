from api.db import get_db
from sqlite3 import Connection, Row
import functools
from flask import g, make_response, abort

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


def check_availability(user_id: int, equipment_id: int, time_slot_id: int) -> bool:
    """This utility function checks if a reservation is valid by checlking if
    the user and equipment are available for a given timeslot. This is function only queries the
    database once instead of the two separate queries in the validate_reservation function.

    Args:
        user_id (int): The ID of the user making the reservation.
        equipment_id (int): The ID of the equipment being reserved.
        time_slot_id (int): The ID of the timeslot being reserved.

    Returns:
        bool: True if the user and equipment are both available, False otherwise.
    """

    # Check if equipment and user is available for a given timeslot
    query = """
            SELECT 
                equipment_id, time_slot_id, user_id
            FROM 
                reservation 
            WHERE
                (equipment_id = ? AND time_slot_id = ?) OR (user_id = ? AND time_slot_id = ?)"""
    db = get_db()
    reservations = db.execute(
        query, (equipment_id, time_slot_id, user_id)).fetchall()
    if len(reservations) > 0:
        return False
    return True


def validate_reservation(user_id: str, equipment_id: str, time_slot_id: str) -> tuple[bool, str]:
    """This utility function validates a reservation request.

    Args:
        user_id (int): The ID of the user making the reservation.
        equipment_id (int): The ID of the equipment being reserved.
        time_slot_id (int): The ID of the timeslot being reserved.

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating whether the reservation is valid,
        and a string containing a message indicating why the reservation is invalid."""
    if not user_id or not equipment_id or not time_slot_id:
        return (False, 'User ID, equipment ID, and timeslot ID are required.')

    if not check_if_resource_exists(resource_name='user', id=int(user_id)):
        return (False, 'User not found.')
    if not check_if_resource_exists(resource_name='equipment', id=int(equipment_id)):
        return (False, 'Equipment not found.')
    if not check_if_resource_exists(resource_name='time_slot', id=int(time_slot_id)):
        return (False, 'Timeslot not found.')

    if not check_if_resource_available(resource_name='equipment', id=int(equipment_id), time_slot_id=int(time_slot_id)):
        return (False, 'Equipment already reserved for this timeslot.')
    if not check_if_resource_available(resource_name='user', id=int(user_id), time_slot_id=int(time_slot_id)):
        return (False, 'User already has a reservation for this timeslot.')
    return (True, 'Reservation is valid.')
