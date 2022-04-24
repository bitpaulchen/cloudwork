import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
    #     'postgres://', 'postgresql://') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')

    print(os.environ)

    if 'RDS_DB_NAME' in os.environ:
        SQLALCHEMY_DATABASE_URI = \
            'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'.format(
                username=os.environ['RDS_USERNAME'],
                password=os.environ['RDS_PASSWORD'],
                host=os.environ['RDS_HOSTNAME'],
                port=os.environ['RDS_PORT'],
                database=os.environ['RDS_DB_NAME'],
            )
    else:
        print("RDS_DB_NAME")
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:12345678@flaskapp.cce4qvbm0cza.us-east-1.rds.amazonaws.com/microblog"
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




