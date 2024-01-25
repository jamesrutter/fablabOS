from typing import Sequence
from flask import current_app
from api.database import db_session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from api.models import Reservation

def get_reservations() -> Sequence[Reservation]:
    stmt = select(Reservation).options(joinedload(Reservation.timeslot), joinedload(Reservation.equipment), joinedload(Reservation.user))
    current_app.logger.debug(
        f'SQL >> {str(stmt)}')
    reservations: Sequence[Reservation] = db_session.execute(stmt).scalars().all()
    current_app.logger.debug(
        'RESERVATION >> Successfully retrieved reservation list.')
    return reservations 