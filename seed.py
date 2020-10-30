"""Seed file to make sample data for users db."""

from models import User, Post, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
user1 = User(first_name='John', last_name='Doe', image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
user2 = User(first_name='Jeremy', last_name='Cale', image_url="https://static.tvmaze.com/uploads/images/medium_portrait/24/60960.jpg")
user3 = User(first_name='Doug', last_name='Gardiner', image_url="https://assets.faceit-cdn.net/avatars/0c024822-580a-4951-ac1e-1acd3655c08f_1551047046710.jpg")

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Add posts
post1 = Post(title="Boring title",content="story content goes here",user_id=1)
post2 = Post(title="Another story",content="story content goes here",user_id=1)
post3 = Post(title="Bad story",content="story content goes here",user_id=1)
post4 = Post(title="Hey noobs, im gonna pwn u",content="teh pwnerer sends his regards",user_id=2)
post5 = Post(title="irl totally lame",content="like the graphics man, totally lame",user_id=2)
post6 = Post(title="I can dance all day",content="JUST TRY AND HIT ME",user_id=3)
post7 = Post(title="Everyone runs faster with a knife",content="everyone knows that, cmon kyle",user_id=3)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.add(post5)
db.session.add(post6)
db.session.add(post7)

db.session.commit()

# Add tags
tag1 = Tag(name="Funny")
tag2 = Tag(name="Sad")
tag3 = Tag(name="Stupid")

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

db.session.commit()

