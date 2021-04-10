from app import app
from unittest import TestCase

app.config['WTF_CSRF_ENABLED'] = False

class FoodieTestCase(TestCase):
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
                "username":"posttest",
                "password":"123",
                "email":"posttest@gmail.com",
                "age":8,
                "gender":"Male",
                "photo_url":"",
                "favorite_business":[]
            }
            res = client.post("/signup", data = data, follow_redirects = True)
            html = res.get_data(as_text = True)
            
            # import pdb
            # pdb.set_trace()

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-outline-danger ml-2">Delete User</button>', html)

