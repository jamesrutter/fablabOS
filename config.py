import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some secret string'
    MAIL_USERNAME = os.environ.get('ACCOUNT_EMAIL')
    MAIL_PASSWORD = os.environ.get('APP_PASSWORD')
    MAIL_SERVER = os.environ.get('SMTP_SERVER')
    MAIL_PORT = os.environ.get('PORT')
    # DATABASE = os.environ.get('DATABASE') or \
    #     'sqlite:///' + os.path.join(basedir, '/data/', 'fablabOS.sqlite')
