import os

from unittest import TestCase
from app import app
from secrets import API_SECRET_KEY
from models import User, Business, FavoriteBusiness, db
from flask import session

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///food_test'
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

class FoodieTestCase(TestCase):
    def setUp(self):
    
        db.drop_all()
        db.create_all()
        
        User.query.delete()
        Business.query.delete()
        FavoriteBusiness.query.delete()

    def tearDown(self):
        "Cleanr up foulded transactions."
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_session(self):
        with app.test_client() as client:
            res = client.get('/')

            self.assertEqual(res.status_code, 200)
            # import pdb
            # pdb.set_trace()
            self.assertNotEqual(session['location'], None)

    def test_getRequest_signup_form(self):
        with app.test_client() as client:
            # Test Get Request for Sign Up Page
            client.get('/')
            res = client.get('/signup')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="text-center" style="margin-top: 1rem;">Sign Up</h1>', html)

    def test_postRequest_signup_form(self):
        with app.test_client() as client:
            client.get('/')
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
            client.get('/')
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
            client.get('/')
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
            self.assertIn('<li><span style="font-weight: 600; color: orange">Email: </span> edit_test@gmail.com</li>', html)

    def test_logout(self):
        with app.test_client() as client:
            client.get('/')
            #test for logout
            res = client.get('/logout', follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Explore Your Favorite & Cool Things <br>In', html)

    def test_user_detail(self):
        with app.test_client() as client:
            client.get('/')
            # Create a user with info shown below
            u1 = User.signup('Jason', '123', 'jason@email.com', 1, '', '', [])
            db.session.add(u1)
            db.session.commit()

            # sign in with the user info above
            signin_data = {            
                "username": 'Jason',
                "password": '123'
            }
            res = client.post("/signin", data = signin_data, follow_redirects = True)
            
            res = client.get("users/Jason")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 style="color: orange;">Items You like:</h3>', html)
            self.assertIn('<li><span style="font-weight: 600; color: orange">Name: </span> Jason</li>', html)

    def test_user_delete(self):
        with app.test_client() as client:
            client.get('/')
            # Delete user
            # Create two users with info shown below
            u1 = User.signup('user1', '123', 'user1@email.com', 18, '', '', [])

            db.session.add(u1)
            db.session.commit()

            # check if non signed user has an access to user delete route 
            res = client.delete("/users/delete")
            self.assertEqual(res.status_code, 405)

            # sign in with user u1
            signin_data = {            
                "username": 'user1',
                "password": '123'
            }

            res = client.post("/signin", data = signin_data, follow_redirects = True)

            # check if a signed user has an access to user delete route 
            res = client.post("/users/delete", follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Explore Your Favorite & Cool Things <br>In', html)

    def test_business_details(self):
        with app.test_client() as client:
            client.get('/')
            # Create a user with info shown below
            b1 = Business(business_id = 'OSZ6bFeCcv4PvUmvuiMEJw', business_name = 'Little Sweet')
            db.session.add(b1)
            db.session.commit()

            res = client.get("foodies/details/OSZ6bFeCcv4PvUmvuiMEJw")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<i class="fab fa-yelp" style="color: #c41200;"></i> More Reviews', html)
            # this item has not been added to user's favourite
            self.assertIn('style="display: inline-block; margin-right: 0.1rem" style="display: inline-block; margin-right: 0.1rem">Add it to Favorite?</a>', html)

    def test_add_business_to_favorites(self):
        with app.test_client() as client:
            client.get('/')

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

            # have user signed in
            signin_data = {            
                "username": "signin_test",
                "password": "123"
            }
            res = client.post("/signin", data = signin_data, follow_redirects = True)

            # Create a business which is added as a favourite one of user signin_test
            b1 = Business(business_id = 'OSZ6bFeCcv4PvUmvuiMEJw', business_name = 'Little Sweet')

            # add business to user's favourite item list
            fav = FavoriteBusiness(username = 'signin_test', business_id = 'OSZ6bFeCcv4PvUmvuiMEJw')

            db.session.add(b1, fav)
            db.session.commit()

            res = client.get('/users/favorites/OSZ6bFeCcv4PvUmvuiMEJw', follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Little Swee', html)
            self.assertIn('<button class="btn btn-outline-danger ml-2">Delete User</button>', html)











    
