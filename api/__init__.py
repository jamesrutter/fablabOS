import os
from config import Config
from flask import Flask
from .errors import handle_404, handle_500, handle_http_exception
from werkzeug.exceptions import HTTPException


def create_app(test_config=None):
    # create and configure the app
    app = Flask(import_name=__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'schedulr.sqlite'),
    # )

    app.config.from_object(Config)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(filename='config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(mapping=test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(name=app.instance_path)
    except OSError:
        pass

    @app.route(rule='/')
    def index():
        return 'fablabOS API 1.0.0'

    from . import db
    db.init_app(app=app)

    from schedulr.reservations import reservations_bp
    app.register_blueprint(blueprint=reservations_bp)

    from schedulr.equipment import equipment_bp
    app.register_blueprint(blueprint=equipment_bp)

    from schedulr.auth import auth_bp
    app.register_blueprint(blueprint=auth_bp)

    from schedulr.auth.users import users_bp
    app.register_blueprint(blueprint=users_bp)

    # register the error handlers
    # app.register_error_handler(HTTPException, handle_http_exception)
    # app.register_error_handler(404, handle_404)
    # app.register_error_handler(500, handle_500)

    return app


app = create_app()
