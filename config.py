from os import environ, path
basedir = path.abspath(path.dirname(__file__))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'some secret string'
    MAIL_USERNAME = environ.get('ACCOUNT_EMAIL')
    MAIL_PASSWORD = environ.get('APP_PASSWORD')
    MAIL_SERVER = environ.get('SMTP_SERVER')
    MAIL_PORT = environ.get('PORT')
    DATABASE = environ.get('SQLALCHEMY_DATABASE_URI')