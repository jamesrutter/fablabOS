from flask import request, render_template
from api.auth.decorators import login_required, admin_required
from . import timeslots
from .controllers import get_timeslots

##############################
## TIMESLOTS VIEW FUNCTIONS ##
##############################


@timeslots.get('/')
def index():
    timeslots = get_timeslots()
    return render_template('index.html', timeslots=timeslots)

