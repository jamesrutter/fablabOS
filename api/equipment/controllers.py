from flask import current_app
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from api.models import Equipment, Reservation
from api.database import db_session
from typing import Sequence

##############################
## EQUIPMENT CRUD FUNCTIONS ##
##############################


def get_equipment_list() -> Sequence[Equipment]:
    stmt = select(Equipment)
    equipment_list: Sequence[Equipment] = db_session.execute(
        stmt).scalars().all()
    return equipment_list


def get_equipment_details(id: int):
    stmt = select(Equipment).where(Equipment.id == id)
    equipment = db_session.execute(stmt).scalar()
    if equipment is None:
        current_app.logger.warning(
            f'EQUIPMENT >> Equipment with id {id} does not exist.')
        return None
    return equipment


def create_equipment(request):
    name = request.form.get('name')
    description = request.form.get('description')

    if not name or not description:
        current_app.logger.warning(
            'EQUIPMENT >> Missing name or description in form data.')
        return None  # Or handle this case as needed

    try:
        new_equipment = Equipment(name=name, description=description)
        db_session.add(new_equipment)
        db_session.commit()

        current_app.logger.info(
            f'EQUIPMENT >> Successfully created equipment with id {new_equipment.id}.')
        return new_equipment
    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(
            f'EQUIPMENT >> Database error occurred while creating equipment: {e}')
        return None


def update_equipment(id: int, request):
    name = request.form.get('name')
    description = request.form.get('description')

    if not name and not description:
        current_app.logger.warning(
            'EQUIPMENT >> Missing both name and description in form data.')
        return None

    try:
        stmt = select(Equipment).where(Equipment.id == id)
        equipment_to_update = db_session.execute(stmt).scalar()

        if equipment_to_update is None:
            current_app.logger.warning(
                f'EQUIPMENT >> Equipment with id {id} does not exist.')
            return None

        if name:
            equipment_to_update.name = name
        if description:
            equipment_to_update.description = description

        db_session.commit()

        return equipment_to_update
    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f'EQUIPMENT >> Error updating equipment: {e}')
        return None


def delete_equipment(id: int):
    try:
        # First, check if the equipment exists
        stmt = select(Equipment).where(Equipment.id == id)
        equipment_to_delete = db_session.execute(stmt).scalar()

        if equipment_to_delete is None:
            current_app.logger.warning(
                f'EQUIPMENT >> Equipment with id {id} does not exist.')
            return False  # Equipment not found

        # Perform the deletion
        db_session.delete(equipment_to_delete)
        db_session.commit()

        current_app.logger.info(f'Successfully deleted equipment id {id}.')
        return True  # Successfully deleted
    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f'EQUIPMENT >> Error deleting equipment: {e}')
        return False  # Deletion failed due to a database error
