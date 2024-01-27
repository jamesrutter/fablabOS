from typing import Sequence
from datetime import datetime
from flask import g, Request, current_app
from sqlalchemy import select
from api.database import db_session
from api.models import Reservation
from api.reservations.validators import validate_reservation


def get_reservations() -> Sequence[Reservation]:
    stmt = select(Reservation)
    reservations: Sequence[Reservation] = db_session.execute(
        stmt).scalars().all()
    return reservations


def get_reservation(id: int) -> Reservation:
    stmt = select(Reservation).where(Reservation.id == id)
    reservation: Reservation = db_session.execute(stmt).scalar_one()
    return reservation


def delete_reservation(id: int):
    stmt = select(Reservation).where(Reservation.id == id)
    reservation: Reservation = db_session.execute(stmt).scalar_one()
    db_session.delete(reservation)
    db_session.commit()


def create_reservation(request: Request) -> tuple[Reservation | None, str | None]:
    time_slot_id = int(request.form['timeslot'])
    equipment_id = int(request.form['equipment'])
    user_id = g.user.id

    # Validate the reservation
    valid, e = validate_reservation(user_id, equipment_id, time_slot_id)
    if not valid:
        return None, e

    # Create the reservation
    reservation = Reservation(
        user_id=user_id,
        equipment_id=equipment_id,
        time_slot_id=time_slot_id,
    )

    db_session.add(reservation)
    db_session.commit()

    # Send confirmation email
    # confirmation_email(reservation)
    return reservation, None


def update_reservation(id: int, request) -> tuple[Reservation | None, str | None]:
    equipment_id = int(request.form['equipment'])
    time_slot_id = int(request.form['timeslot'])
    user_id = g.user.id

    # Validate the reservation
    valid, msg = validate_reservation(user_id, equipment_id, time_slot_id, reservation_id=id)
    if not valid:
        current_app.logger.debug(msg)
        return None, msg

    try:
        # Select the exisiting reservation
        stmt = select(Reservation).where(Reservation.id == id)
        reservation: Reservation = db_session.execute(stmt).scalar_one()

        # Update the reservation
        reservation.equipment_id = equipment_id
        reservation.time_slot_id = time_slot_id

        db_session.commit()
        return reservation, None
    except Exception:
        msg = "Error updating reservation"
        current_app.logger.debug(msg)
        db_session.rollback()
        return None, msg
