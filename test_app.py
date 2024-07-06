import unittest
from app import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_latest_data(self):
        response = self.app.get('/api/latest')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
