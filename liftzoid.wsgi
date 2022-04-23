import sys
sys.path.insert(0, '/var/www/html/cloudwork')
from flaskapp import app as application
from app import create_app, db, cli
app =