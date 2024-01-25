from typing import Sequence
from flask import current_app
from sqlalchemy import select
from api.models import TimeSlots
from api.database import db_session

##############################
## TIMESLOT CRUD FUNCTIONS ##
##############################


def get_timeslots() -> Sequence[TimeSlots]:
    stmt = select(TimeSlots) 
    timeslots: Sequence[TimeSlots] = db_session.execute(stmt).scalars().all()
    current_app.logger.debug(
        'TIMESLOT >> Successfully retrieved timeslot list.')
    return timeslots
