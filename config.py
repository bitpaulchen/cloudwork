import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# 定义一些配置项

import boto3


class Config(object):
    print(os.environ)
    SECRET_KEY = "12345678"
    AWS_RDS_HOST = "flaskapp.cce4qvbm0cza.us-east-1.rds.amazonaws.com"
    AWS_RDS_NAME = "root"
    AWS_RDS_PWD = "12345678"
    AWS_RDS_DATABASE = "cloudwork"

    AWS_ACCESS_KEY = "ASIA2ZZJ23VSLSFCVKEK"
    AWS_SECRET_KEY = "BquhbOF0uurQA51r/cIgS5AL3Y5U8QZtAGX1ljkx"
    AWS_SESSION_TOKEN = "FwoGZXIvYXdzEPT//////////wEaDH0w2XloS8xfKW9hNiLNAW7/SfOpRlCDSi84XAiK4/uxTOxKrUW67W7r4Eu7L2efdyw1jhP0M4T6AF8UNYExsLa86vrhiy06KluVvERFs/d9mmSzP1tMe5ltKRTIwrG2l4El0Fye0k68ITV08M3+XX+GLrDQytDONMzCdv3SNsSIj0EUoRNK9cjGeqPGhojjXFmC4ZxW1skOY7i+a9vKKDozXZNEd9r5NinYLCFds/D6Zv/clRUPu4lU7t2b5CjX6coPKY4h3douIHxyzm0huQqqFCLnAC3xB45CSBQo4qidkwYyLVYPbhFFM0g3nuFrMH8lujGmZEAjjfMkpibc9q+E9cVEsZse9r5vX5X9Q8eEvw=="
    REGION = "us-east-1"

    API_GATEWAY = {
        "article_body_get": "https://rutkf5uzhl.execute-api.us-east-1.amazonaws.com/getArticle",
        "article_body_create": "https://rutkf5uzhl.execute-api.us-east-1.amazonaws.com/postArticle",
    }


    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{password}@{host}/{database}".format(
        user=AWS_RDS_NAME,
        password=AWS_RDS_PWD,
        host=AWS_RDS_HOST,
        database=AWS_RDS_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LANGUAGES = ['en', 'es']

    POSTS_PER_PAGE = 25




