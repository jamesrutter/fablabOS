from flask import Blueprint

reservations = Blueprint('reservations', __name__)

from . import views