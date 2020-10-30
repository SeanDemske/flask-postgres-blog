from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:developer@localhost:5432/blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User"""

    def setUp(self):
        """Add sample User"""

        Post.query.delete()
        User.query.delete()
        Tag.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()


        post = Post(title="Sample Post",content="Sample Content",user_id=user.id)
        db.session.add(post)
        db.session.commit()

        tag = Tag(name="devtag")
        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id
        self.post_id = post.id
        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


############################
# /////////////////#############
#   USER ROUTES        ###########
# /////////////////#############
###############################


    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {
                "firstName": "Mr", 
                "lastName": "Developer",
                "profilePic": ""
            }
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Mr Developer", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {
                "firstName": "Updated",
                "lastName": User.query.get(self.user_id).last_name,
                "profilePic": User.query.get(self.user_id).image_url
            }
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Updated User", html)


############################
# /////////////////#############
#   POST ROUTES        ###########
# /////////////////#############
###############################

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sample Content', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {
                "title": "Test", 
                "content": "Sample post",
                "user_id": self.user_id
            }

            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test", html)
            self.assertIn("Sample post", html)

    def test_edit_post(self):
        with app.test_client() as client:
            d = {
                "title": "Updated Title", 
                "content": "Updated Content",
                "user_id": self.user_id
            }
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Updated Title", html)
            self.assertIn("Updated Content", html)

############################
# /////////////////#############
#   Tag ROUTES        ###########
# /////////////////#############
###############################

    def test_list_tags(self):
        with app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tags', html)
            self.assertIn('Add tag', html)

    def test_show_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'Posts tagged as "devtag"', html)

    def test_add_tag(self):
        with app.test_client() as client:
            d = {
                "tagName": "created_tag"
            }

            resp = client.post(f"/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("created_tag", html)

    def test_edit_tag(self):
        with app.test_client() as client:
            d = {
                "tagName": "updated_tag"
            }
            resp = client.post(f"/tags/{self.tag_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("updated_tag", html)


