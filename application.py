from app import create_app
import os

application = create_app()





if __name__ == '__main__':
    application.run('0.0.0.0', port=int(os.environ.get("PORT", 5000)))

