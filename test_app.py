from app import app
from unittest import TestCase

class FoodieTestCase(TestCase):
    def test_signup_form(self):
        with app.test_client() as client:
            import pdb
            pdb.set_trace()
            # res = client.get('/signup')
            # html = res.get_data(as_test = True)

            # self.assertEqual(res.status_code, 200)