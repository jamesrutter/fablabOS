from api import create_app, db_session
import os
import click

app = create_app(os.getenv('FLASK_CONFIG') or None)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db_session)


@click.command('test')
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    print(tests)
    unittest.TextTestRunner(verbosity=2).run(tests)


app.run(debug=True)
