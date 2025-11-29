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
    
    def test_register(self, username, email, password):
        return self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password
        ), follow_redirects=True)

    def test_login(self, username, password):
        return self.app.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    def test_logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.test_login('admin', 'default')
        assert b'You were logged in' in rv.data
        rv = self.test_logout()
        assert b'You were logged out' in rv.data
        rv = self.test_login('adminx', 'default')
        assert b'Invalid username' in rv.data
        rv = self.test_login('admin', 'defaultx')
        assert b'Invalid password' in rv.data

if __name__ == '__main__':
    unittest.main()