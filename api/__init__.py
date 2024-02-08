import os
from logging.config import dictConfig
from config import Config, log_settings
from flask import Flask, render_template
from api.database import db_session
from api.controllers import get_reservations

# TODO: Rename this package to "schedulr" and update all references to it.


def create_app(test_config=None):

    # Configure logging
    dictConfig(log_settings)

    app = Flask(__name__, instance_relative_config=True)
    app.logger.debug('Creating app....')

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    app.logger.debug('Configuring app....')
    app.logger.debug(f'SECRET_KEY:{Config.SECRET_KEY}')
    
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

    from api.auth import auth as auth_bp
    app.register_blueprint(blueprint=auth_bp, url_prefix='/auth')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
