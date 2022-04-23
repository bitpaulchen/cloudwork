from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task, Comment
from datetime import datetime
import random, string

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task}


def userbatch():

    for i in range(2,100):
        print(i)
        user = User(username="susun%s"%i, email="susun{i}@email.com".format(i=i))
        user.set_password("1234")
        user.about_me = "i am susun{i} !".format(i=i)
        user.last_seen = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(user)
    db.session.commit()

def follow():
    sql = "insert into followers (follower_id, followed_id) VALUES "
    values = []
    for _ in range(200):
        values.append("(%s, %s) " % (random.randint(57,154), random.randint(57,154)))
    sql = sql + ",".join(values)

def randomword(length):
   letters = string.ascii_lowercase + "        "
   return ''.join(random.choice(letters) for i in range(length))


def post():
    for i in range(2,100):
        print(i)
        body = randomword(70)
        post = Post(body=body, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user_id = random.randint(57,154))
        db.session.add(post)
    db.session.commit()



def comment():
    for i in range(1,300):
        print(i)
        comment = Comment(user_id=random.randint(57,154),body  = randomword(20),  post_id=random.randint(1,198))
        db.session.add(comment)
    db.session.commit()
