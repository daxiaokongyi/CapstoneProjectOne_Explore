from app import app
from unittest import TestCase
from models import db, User, Business, FavoriteBusiness

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///foodies_test'
app.config['SQLALCHEMY_ECHO'] = False
# app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

USER_DATA = {
    "username": "test",
    "password": "123",
    "email": "test@gmail.com",
    "gender": "Male",
    "age": 18
}

class FoodieTestCase(TestCase):
    def setUp(self):
        """Make Demo Data"""
        User.query.delete()

        new_user = User(**USER_DATA)
        db.session.add(new_user)
        db.session.commit()

        self.new_user = new_user

    def tearDown(self):
        """Clean up foulded transactions"""
        db.session.rollback()

    def test_getRequest_signup_form(self):
        with app.test_client() as client:
            # Test Get Request for Sign Up Page
            # import pdb
            # pdb.set_trace()
            res = client.get('/signup')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="text-center" style="margin-top: 1rem;">Sign Up</h1>', html)

    def test_postRequest_signup_form(self):
        with app.test_client() as client:
        # Test Get Request for Sign Up Page
            app.config['WTF_CSRF_ENABLED'] = False

            res = client.post(
                '/signup', 
                data = dict(
                    username = "newtest",
                    password = "123",
                    email = "newtest@gmail.com",
                    gender = "Male",
                    age = 8
                ), 
                follow_redirects=True
            )
            html = res.get_data(as_text = True)
            
            # import pdb
            # pdb.set_trace()

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-outline-danger ml-2">Delete User</button>', html)


