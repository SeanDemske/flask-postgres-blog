"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag, DEFAULT_IMG_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:developer@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

##############################
# /////////////////#############
#   USER ROUTES        #########
# /////////////////#############
##############################

@app.route("/")
def home_page():
    """Redirect to users listing"""

    return redirect("/users")


@app.route("/users")
def list_users():
    """List users and show add form."""

    users = User.query.all()
    return render_template("index.html", users=users)


@app.route("/users/new")
def add_user_form():
    """Add form for new users to fill out"""

    return render_template("user_add.html")


@app.route("/users/new", methods=["POST"])
def create_user():
    """List users and show add form."""

    first = request.form['firstName']
    last = request.form['lastName']
    avi = request.form['profilePic']

    if avi:
        new_user = User(first_name=first, last_name=last, image_url=avi)
    else:
        new_user = User(first_name=first, last_name=last)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def user_info(user_id):
    """Show's user information"""

    user = User.query.get(user_id)
    return render_template("user_detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Displays edit user form"""

    user = User.query.get(user_id)
    return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit a users information"""

    user = User.query.get(user_id)

    first = request.form['firstName']
    last = request.form['lastName']
    avi = request.form['profilePic']

    user.first_name = first
    user.last_name = last
    if avi:
        user.image_url = avi

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes user from database and redirects to /users"""

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

############################
# /////////////////#############
#   POST ROUTES        ###########
# /////////////////#############
###############################


@app.route("/users/<int:user_id>/posts/new")
def create_post_form(user_id):
    """Displays create post form"""

    user = User.query.get(user_id)
    return render_template("post_add.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    """Handles post form submission"""

    user = User.query.get(user_id)

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title,content=content,user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/posts/{new_post.id}")


@app.route("/posts/<int:post_id>")
def display_post(post_id):
    """Displays a users post"""

    post = Post.query.get(post_id)

    return render_template("post_detail.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Displays an edit post form"""

    post = Post.query.get(post_id)
    all_tags = Tag.query.all()

    return render_template("post_edit.html", post=post, all_tags=all_tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Edit a users information"""

    post = Post.query.get(post_id)

    title = request.form['title']
    content = request.form['content']
    checked_tags = request.form.getlist("tags")
    
    if title and content:
        post.title = title
        post.content = content

    post.tags = Tag.query.filter(Tag.id.in_(checked_tags)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post from the database"""

    post = Post.query.get(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


############################
# /////////////////#############
#   TAG ROUTES        ###########
# /////////////////#############
###############################


@app.route("/tags")
def show_tags():
    """Show all tags"""

    tags = Tag.query.all()

    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_detail(tag_id):
    """Show all tags"""

    tag = Tag.query.get(tag_id)

    return render_template("tag_detail.html", tag=tag)


@app.route("/tags/new")
def show_tag_create_form():
    """Shows a form to create a tag"""

    posts = Post.query.all()

    return render_template("tag_add.html", posts=posts)


@app.route("/tags/new", methods=["POST"])
def create_tag():
    """Create selected tag"""

    tag_name = request.form["tagName"]
    new_tag = Tag(name=tag_name)
    checked_posts = request.form.getlist("posts")

    db.session.add(new_tag)
    db.session.commit()

    for checked_post in checked_posts:
        posttag = PostTag(post_id=checked_post, tag_id=new_tag.id)
        db.session.add(posttag)
        db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_tag_edit_form(tag_id):
    """Shows a form to edit selected tag"""

    tag = Tag.query.get(tag_id)

    return render_template("tag_edit.html", tag=tag)



@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Update edited tag"""

    update_tag = Tag.query.get(tag_id)
    tag_name = request.form["tagName"]
    update_tag.name = tag_name

    db.session.add(update_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete selected tag"""

    delete_tag = Tag.query.get(tag_id)

    db.session.delete(delete_tag)
    db.session.commit()

    return redirect("/tags")
