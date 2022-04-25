import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    print(os.environ)

    # database


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
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://cloudsample:12345678@aat00fh6fq0ent.cce4qvbm0cza.us-east-1.rds.amazonaws.com/ebdb"

    # apigateway
    AWS_API_GATEWAY_POSTS = "https://rutkf5uzhl.execute-api.us-east-1.amazonaws.com/"
    AWS_API_GATEWAY_COMMENTS = "https://5r0by4zgua.execute-api.us-east-1.amazonaws.com"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    POSTS_PER_PAGE = 25


