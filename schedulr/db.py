import sqlite3
import click
from flask import current_app, g, Flask, jsonify, Response
from sqlite3 import DatabaseError, Cursor
from werkzeug.security import generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            database=current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # open_resource() opens a file relative to the flaskr package, which is useful since you won’t necessarily know where that location is when deploying the application later. get_db returns a database connection, which is used to execute the commands read from the file.
    with current_app.open_resource(resource='schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command(name='init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    # click.command() defines a command line command called init-db that calls the init_db function and shows a success message to the user. You can read Command Line Interface to learn more about writing commands.
    init_db()
    click.echo(message='Initialized the database.')


def init_app(app: Flask):
    # app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    # app.cli.add_command() adds a new command that can be called with the flask command.
    app.cli.add_command(cmd=init_db_command)
    app.cli.add_command(cmd=seed_db)


def get_all_data_from_table(table_name) -> Response:
    """
    Fetches all records from a specified table in the database.

    Args:
        table_name (str): The name of the table to fetch records from.

    Returns:
        list: A list of dictionaries where each dictionary represents a record in the table.
        If an error occurs, returns an error message with a 500 status code.
    """
    try:
        db = get_db()
        query = f"SELECT * FROM {table_name}"
        rows = db.execute(query).fetchall()
        return jsonify([dict(row) for row in rows])
    except DatabaseError as e:
        return jsonify({'error': e.args[0]}, 500)


@click.command(name='seed-db')
def seed_db():
    """
    Seeds the database with timeslot records.
    """
    init_db()  # Initialize the database if it doesn't exist.
    db = get_db()

    timeslots_queries = [
        "INSERT INTO time_slot (start_time, end_time) VALUES ('09:00:00', '10:00:00')",
        "INSERT INTO time_slot (start_time, end_time) VALUES ('10:00:00', '11:00:00')",
        "INSERT INTO time_slot (start_time, end_time) VALUES ('11:00:00', '12:00:00')",
        "INSERT INTO time_slot (start_time, end_time) VALUES ('12:00:00', '13:00:00')",
        "INSERT INTO time_slot (start_time, end_time) VALUES ('13:00:00', '14:00:00')",
        "INSERT INTO time_slot (start_time, end_time) VALUES ('14:00:00', '15:00:00')",
        "INSERT INTO time_slot (start_time, end_time) VALUES ('15:00:00', '16:00:00')",
        "INSERT INTO time_slot (start_time, end_time) VALUES ('16:00:00', '17:00:00')",
    ]

    password_hash = generate_password_hash(
        password='password')  # default password for all users

    users_queries = [
        f"INSERT INTO user (username, password, role) VALUES ('james', '{password_hash}', 'admin')",
        f"INSERT INTO user (username, password, role) VALUES ('jenn', '{password_hash}', 'user')",
        f"INSERT INTO user (username, password, role) VALUES ('lucia', '{password_hash}', 'user')",
    ]

    equipment_queries = [
        "INSERT INTO equipment (name, description) VALUES ('Laser Cutter A', 'High precision laser cutter suitable for intricate designs.')",
        "INSERT INTO equipment (name, description) VALUES ('Laser Cutter B', 'High precision laser cutter suitable for intricate designs.')",
        "INSERT INTO equipment (name, description) VALUES ('3D Printer A', 'Versatile 3D printer for prototyping and small-scale production.')",
        "INSERT INTO equipment (name, description) VALUES ('3D Printer B', 'Versatile 3D printer for prototyping and small-scale production.')",
        "INSERT INTO equipment (name, description) VALUES ('CNC Mill A', 'Computer-controlled milling machine for cutting and engraving.')",
    ]

    reservations_queries = [
        # 09:00-10:00, James, Laser Cutter A
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (1, 1, 1)",
        # 10:00-11:00, Jenn, Laser Cutter B
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (2, 2, 2)",
        # 11:00-12:00, Lucia, 3D Printer A
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (3, 3, 3)",
        # 12:00-13:00, James, 3D Printer B
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (4, 1, 4)",
        # 13:00-14:00, Jenn, CNC Mill A
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (5, 2, 5)",
        # 14:00-15:00, Lucia, Laser Cutter A
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (6, 3, 1)",
        # 15:00-16:00, James, Laser Cutter B
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (7, 1, 2)",
        # 16:00-17:00, Jenn, 3D Printer A
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (8, 2, 3)",
        # 09:00-10:00 next day, Lucia, 3D Printer B
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (1, 3, 4)",
        # 10:00-11:00 next day, James, CNC Mill A
        "INSERT INTO reservation (time_slot_id, user_id, equipment_id) VALUES (2, 1, 5)",
    ]

    for query in timeslots_queries:
        try:
            db.execute(query)
            db.commit()
            click.echo(message='Seeded database with timeslots.')

        except DatabaseError as e:
            print(e.args[0])
            db.rollback()

    for query in users_queries:
        try:
            db.execute(query)
            db.commit()
            click.echo(message='Seeded database with users.')

        except DatabaseError as e:
            print(e.args[0])
            db.rollback()

    for query in equipment_queries:
        try:
            db.execute(query)
            db.commit()
            click.echo(message='Seeded database with equipment data.')

        except DatabaseError as e:
            print(e.args[0])
            db.rollback()

    for query in reservations_queries:
        try:
            db.execute(query)
            db.commit()
            click.echo(message='Seeded database with reservations.')

        except DatabaseError as e:
            print(e.args[0])
            db.rollback()
