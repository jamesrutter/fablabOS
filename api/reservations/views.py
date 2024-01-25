# from flask import request
# from api.auth.decorators import login_required
# from .validators import validate_reservation
# from api.auth.decorators import owner_required
# from api.mail import confirmation_email

from flask import render_template
from api.reservations import reservations
from api.reservations.controllers import get_reservations

###############################
# RESERVATION VIEW FUNCTIONS ##
###############################


@reservations.get('/')
def index():
    reservations = get_reservations()
    return render_template('reservations/index.html', reservations=reservations)
