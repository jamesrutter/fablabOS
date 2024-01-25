from dotenv import load_dotenv
from os import environ, path
basedir = path.abspath(path.dirname(__file__))

load_dotenv(path.join(basedir, '.env'))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'some secret string'
    MAIL_USERNAME = environ.get('ACCOUNT_EMAIL')
    MAIL_PASSWORD = environ.get('APP_PASSWORD')
    MAIL_SERVER = environ.get('SMTP_SERVER')
    MAIL_PORT = environ.get('PORT')
    DATABASE = environ.get('SQLALCHEMY_DATABASE_URI')


log_settings = {
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
}