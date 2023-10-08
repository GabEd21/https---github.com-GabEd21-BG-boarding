import unittest
from app import app, add_text, add_payment
import MySQLdb.cursors

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.post('/pythonlogin/', data=dict(username='admin', password='admin'), follow_redirects=True)
        self.assertIn(b'Test', response.data)

    def test_add_boarder(self):
        response = self.app.get('/add_boarder')
        self.assertEqual(response.status_code, 200)

    def test_view_boarder(self):
        response = self.app.get('/view_boarder')
        self.assertEqual(response.status_code, 302)  

    def test_account_student(self):
        response = self.app.get('/account_student?username=testuser')
        self.assertEqual(response.status_code, 302) 

    def test_create_payment(self):
        response = self.app.get('/add_payment')
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
