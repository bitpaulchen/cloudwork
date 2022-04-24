from app import create_app, db, cli
from app.models import User, Post

application = create_app()
# cli.register(app)





if __name__ == '__main__':
    application.run()
