import os
from logging.config import dictConfig
from config import Config, log_settings
from flask import Flask, render_template
from api.database import db_session 
from api.controllers import get_reservations


def create_app(test_config=None):

    # Configure logging
    dictConfig(log_settings)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_object(Config)
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route(rule='/')
    def index():
        return render_template('index.html')

    from api.reservations import reservations as reservations_bp
    app.register_blueprint(blueprint=reservations_bp,
                           url_prefix='/reservations')

    from api.equipment import equipment as equipment_bp
    app.register_blueprint(equipment_bp, url_prefix='/equipment')

    # from api.auth import auth as auth_bp
    # app.register_blueprint(blueprint=auth_bp, url_prefix='/auth')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
