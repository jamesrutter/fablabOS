from flask import current_app
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from api.database import db_session
from api.models import Reservation, Equipment, User

#############################################################
###################### HELPER FUNCTIONS #####################
#############################################################


def check_if_resource_exists(id: int) -> bool:
    """This utility function checks if a resource is available for a given timeslot.

    Args:
        id: The ID of the resource to check.

    Returns:
        bool: True if the resource is available for the timeslot, False otherwise.
    """
    try: 
        stmt = select(Equipment).where(Equipment.id == id)
        equipment = db_session.execute(stmt).scalar_one()
        if equipment:
            return True
        return False
    except NoResultFound:
        current_app.logger.debug("Error checking if resource exisits: No Result Found")
        return False

def check_if_user_exists(id: int) -> bool:
    """This utility function checks if a user exists.

    Args:
        id (int): The ID of the user to check.
    Returns:
        bool: True if the resource is available for the timeslot, False otherwise.
    """
    try:
        stmt = select(User).where(User.id == id)
        user = db_session.execute(stmt).scalar_one()
        if user:
            return True
        return False
    except NoResultFound:
        current_app.logger.debug("Error checking if user exists: No Result Found")
        return False


def check_if_resource_available(resource_id: int, time_id: int) -> bool:
    """This utility function checks if a resource is available for a given timeslot.

    Args:
        resource(Equipment): The resource to check.
        time(TimeSlots): The timeslot to check.

    Returns:
        bool: True if the resource is available for the timeslot, False otherwise.
    """
    try:
        stmt = select(Reservation).where(Reservation.equipment_id == resource_id).where(Reservation.time_slot_id == time_id)
        reservations = db_session.execute(stmt).scalar_one_or_none()
        if reservations:
            return False
        return True
    except NoResultFound:
        current_app.logger.debug("Error checking if resource is available: No Result Found")
        return False


def check_if_user_available(user_id: int, time_id: int) -> bool:
    """This utility function checks if a user is available for a given timeslot.
    This is done in order to prevent double-booking a user for a given timeslot.
    Assumption is that users can only reserve one resource at a time.

    Args:
        user(User): The user to check.
        time(TimeSlots): The timeslot to check.
    Returns:
        bool: True if the user is available for the timeslot, False otherwise.
    """
    try:
        stmt = select(Reservation).where(Reservation.user_id == user_id).where(Reservation.time_slot_id == time_id)
        reservations = db_session.execute(stmt).scalar_one_or_none()
        if reservations:
            return False
        return True
    except NoResultFound:
        current_app.logger.debug("Error checking if user is available: No Result Found")
        return False


def validate_reservation(user_id: int, equipment_id: int, time_slot_id: int, reservation_id: int | None = None) -> tuple[bool, str]:
    if not check_if_user_exists(user_id):
        return False, "User does not exist."
    if not check_if_resource_exists(equipment_id):
        return False, "Equipment does not exist."

    # Allow updates to existing reservation without conflicting with itself
    if reservation_id is not None:
        return True, "Update to reservation is valid."

    # New reservation validation
    if not check_if_user_available(user_id, time_slot_id):
        return False, "User is not available for the selected timeslot."
    if not check_if_resource_available(equipment_id, time_slot_id):
        return False, "Equipment is not available for the selected timeslot."
    return True, "The reservation is valid."