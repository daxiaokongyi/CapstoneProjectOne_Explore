from unittest import TestCase
from app import app
from models import User, db
from flask import session

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///food_test'
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()
User.query.delete()

class FoodieTestCase(TestCase):
    def setUp(self):
        User.query.delete()

    def tearDown(self):
        "Cleanr up foulded transactions."
        db.session.rollback()

    def test_getRequest_signup_form(self):
        with app.test_client() as client:
            # Test Get Request for Sign Up Page
            res = client.get('/signup')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="text-center" style="margin-top: 1rem;">Sign Up</h1>', html)

    def test_postRequest_signup_form(self):
        with app.test_client() as client:
            data = {            
                "username":"numberone",
                "password":"123",
                "email":"numberone@gmail.com",
                "age":8,
                "gender":"male",
                "photo_url":"",
                "favorite_business":[]
            }
            res = client.post("/signup", data = data, follow_redirects = True)
            html = res.get_data(as_text = True)
            
            # import pdb
            # pdb.set_trace()

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-outline-danger ml-2">Delete User</button>', html)

    def test_postRequest_signin_form(self):
        with app.test_client() as client:
            # Sign up first and save user signin_test into the database
            data = {            
                "username":"signin_test",
                "password":"123",
                "email":"signin_test@gmail.com",
                "age":8,
                "gender":"male",
                "photo_url":"",
                "favorite_business":[]
            }
            res = client.post("/signup", data = data, follow_redirects = True)

            # Test if user can sign in
            signin_data = {            
                "username": "signin_test",
                "password": "123"
            }
            res = client.post("/signin", data = signin_data, follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 style="color: orange;">Items You like:</h3>', html)
            self.assertIn('<li><span style="font-weight: 600; color: orange">Name: </span> signin_test</li>', html)

    def test_postRequest_edit_form(self):
        with app.test_client() as client:
            # Sign up first and save user edit_test into the database
            data = {            
                "username":"edit_test",
                "password":"123",
                "email":"signin_test@gmail.com",
                "age":8,
                "gender":"male",
                "photo_url":"",
                "favorite_business":[]
            }
            res = client.post("/signup", data = data, follow_redirects = True)

            # Test if users can edit their infos
            edit_data = {            
                "password": "123",
                "age": 6,
                "email": "edit_test@gmail.com"
            }
            res = client.post("/edit", data = edit_data, follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<li><span style="font-weight: 600; color: orange">Email: </span> edit_test@gmail.com</li>',html)

    def test_postRequest_edit_form(self):
        with app.test_client() as client:
            # City name should not be on the homepage while running Geolocation API at the first time
            res = client.get('/')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Explore Your Favorite & Cool Things <br>In <span id="city"></span></h1>',html)

    
