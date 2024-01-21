import os
from api.config import Config
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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
        app.logger.info(msg='API Index Route')
        return {'status': 'success', 'message': 'fablabOS API 0.x.x. Warning! This API is under active and rapid development.'}, 200

    from . import db
    db.init_app(app=app)

    from api.reservations import reservations as reservations_bp
    app.register_blueprint(blueprint=reservations_bp,
                           url_prefix='/reservations')

    from api.equipment import equipment as equipment_bp
    app.register_blueprint(equipment_bp, url_prefix='/equipment')

    from api.auth import auth_bp, users_bp
    app.register_blueprint(blueprint=auth_bp)
    app.register_blueprint(blueprint=users_bp)

    return app


app = create_app()
