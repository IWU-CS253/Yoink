import os
import app as flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        flaskr.app.config["WTF_CSRF_ENABLED"] = False
        self.app = flaskr.app.test_client()

        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    # Helper: full registration including OTP
    def complete_registration(self, username, email, password):
        self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password
        ), follow_redirects=True)

        # Retrieve OTP from DB
        with flaskr.app.app_context():
            db = flaskr.get_db()
            row = db.execute("SELECT code FROM otp WHERE email = ?", (email,)).fetchone()
            otp = row["code"]

        return self.app.post('/send-otp', data=dict(
            username=username,
            email=email,
            password=password,
            otp=otp,
        ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.post('/logout', follow_redirects=True)

    def test_login_logout(self):
        self.complete_registration('admin', 'admin@iwu.edu', 'default')
        rv = self.login('admin', 'default')
        assert b'Welcome, admin' in rv.data
        rv = self.logout()
        assert b'Logged out.' in rv.data
        rv = self.login('adminx', 'default')
        assert b'"Invalid username or password.' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'"Invalid username or password.' in rv.data

if __name__ == '__main__':
    unittest.main()