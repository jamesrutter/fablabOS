from flask import Blueprint

timeslots = Blueprint('timeslots', __name__, template_folder='templates')

from . import views