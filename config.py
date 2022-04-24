import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
    #     'postgres://', 'postgresql://') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/microblog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = "smtp.126.com"
    MAIL_PORT = 25
    MAIL_USE_TLS = 1
    MAIL_USERNAME = "chengpemgbit@126.com"
    MAIL_PASSWORD = "BMIMZRJOKOJTWWNE"
    ADMINS = ['chengpemgbit@126.com']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    POSTS_PER_PAGE = 25




