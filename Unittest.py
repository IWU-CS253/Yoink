import os
import app as flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])
    
    def register(self, username, email, password):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()