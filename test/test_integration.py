import unittest
from app import app 

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_showSummary(self):
        response = self.app.post('/showSummary', data={'email': 'john@simplylift.co'})
        self.assertIn(b'Welcome', response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    def test_showSummary_invalid_email(self):   
        response = self.app.post('/showSummary', data={'email':'invalid_email'})
        self.assertIn(b"Email non trouvé", response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
