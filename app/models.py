from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
import requests
from requests.structures import CaseInsensitiveDict
import json



followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(200))
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5("xxxxx".lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class Post(db.Model):
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    post_uid = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    short_desc = db.Column(db.Text)

    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def get_body(self):
        print("get body:", self.post_uid)


        try:
            apipath = current_app.config["API_GATEWAY"]["article_body_get"]
            response = requests.get(apipath,params={'ids': self.post_uid} )
            res = response.json()
            if len(res)>0:
                return res[0].get("body", "no content, cur_post_uid" + self.post_uid)
            return ''
        except Exception as  e:
            print("Post.get_body error, cur_post_uid:",self.post_uid,  e)
            return  ''

    def post_body(self, body):
        try:
            apipath = current_app.config["API_GATEWAY"]["article_body_create"]
            data = '{"body":"%s"}' % body
            headers = CaseInsensitiveDict()
            headers["Content-Type"] = "application/json"
            response = requests.post(apipath,  headers = headers, data=data)
            print(response)
            res = response.json()
            return res.get('uid', '')
        except Exception as  e:
            print("Post.post_body error,",self.post_uid)
            return  ''


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    user = db.relationship('User', backref='comments')


    def __repr__(self):
        return '<Comment {} comment on {} :  {}>'.format(self.user_id, self.post_id, self.body)






