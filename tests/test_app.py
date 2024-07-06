import unittest
import sys
import os

# Add the project directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_latest_data(self):
        response = self.app.get('/api/latest')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('15 mins', data)
        self.assertIn('30 mins', data)
        self.assertIn('1 hour', data)
        self.assertIn('accuracy', data)

if __name__ == "__main__":
    unittest.main()
