# error_handlers.py in yourpackage/subpackage

from flask import jsonify
from flask.typing import ResponseReturnValue
from werkzeug.exceptions import HTTPException, NotFound, InternalServerError


def handle_http_exception(e) -> ResponseReturnValue:
    """Return JSON for HTTP errors."""
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


def handle_404(e: NotFound) -> ResponseReturnValue:
    """Custom handler for 404 error."""
    return jsonify(error="The requested resource was not found"), 404


def handle_500(e) -> ResponseReturnValue:
    """Custom handler for 500 error."""
    return jsonify(error="An internal server error occurred"), 500

# ... Add other error handlers as needed ...
