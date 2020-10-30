"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMG_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50),
                    nullable=False,
                    unique=False)
    last_name = db.Column(db.String(50),
                    nullable=False,
                    unique=False)
    image_url = db.Column(db.Text,
                    nullable=False,
                    default=DEFAULT_IMG_URL)

    posts = db.relationship("Post", backref="user")


class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(100),
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.DateTime,
                    nullable=False,
                    default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                    db.ForeignKey("users.id"),
                    nullable=False)

    tags = db.relationship('Tag',
                               secondary='post_tag',
                               backref='posts')


class PostTag(db.Model):
    """M to M table for posts and tags"""

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,
                    db.ForeignKey("posts.id"),
                    nullable=False,
                    primary_key=True)
    
    tag_id = db.Column(db.Integer,
                    db.ForeignKey("tags.id"),
                    nullable=False,
                    primary_key=True)


class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(50),
                    nullable=False,
                    unique=True)





    