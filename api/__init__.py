import os
from logging.config import dictConfig
from config import Config
from flask import Flask, render_template

# IMPORT EXTENSTIONS HERE (e.g., SQLAlchemy, Flask-Mail, etc.)
# Instantiate the extensions here (e.g., db = SQLAlchemy())


def create_app(test_config=None):

    # Configure logging
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    })

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set the default configuration

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'api.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app=app)

    @app.route(rule='/')
    def index():
        app.logger.info(msg='API Index Route')
        return render_template('index.html')

    from api.reservations import reservations as reservations_bp
    app.register_blueprint(blueprint=reservations_bp,
                           url_prefix='/reservations')

    from api.equipment import equipment as equipment_bp
    app.register_blueprint(equipment_bp, url_prefix='/equipment')

    from api.auth import auth as auth_bp
    app.register_blueprint(blueprint=auth_bp, url_prefix='/auth')

    return app
