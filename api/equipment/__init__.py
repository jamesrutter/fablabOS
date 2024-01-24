from flask import Blueprint

equipment = Blueprint('equipment', __name__, template_folder='templates')

from . import views