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

    def test_register(self):
        ra = self.register('admin', 'admin@iwu.edu', 'default')
        assert b'You were registered' in ra.data

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert b'Welcome, row[username]' in rv.data
        rv = self.logout()
        assert b'Logged out.' in rv.data
        rv = self.login('adminx', 'default')
        assert b'"Invalid username or password.' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'"Invalid username or password.' in rv.data

if __name__ == '__main__':
    unittest.main()