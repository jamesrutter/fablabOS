import os
from config import Config
from flask import Flask


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

    return app


app = create_app()
