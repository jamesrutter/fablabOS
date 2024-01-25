from flask import Blueprint

reservations = Blueprint('reservations', __name__, template_folder='templates')

from . import views