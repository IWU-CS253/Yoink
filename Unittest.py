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

    def complete_registration(self, username, email, password):
        self.app.post('/register', data=dict(
            username=username,
            email=email,
            password=password
        ), follow_redirects=True)

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
    
    def create_item(self, title, description, category, condition, location, contact, image):
        return self.app.post('/items/new', data=dict(
            title = title,
            description = description,
            category = category,
            condition = condition,
            location = location,
            contact = contact,
            image = image
        ), follow_redirects=True)

    def edit(self, title, description, category, condition, location, contact, image):
        with flaskr.app.app_context():
            db = flaskr.get_db()
            item = db.execute("SELECT * FROM items").fetchone()
            item_id = item["id"]
            return self.app.post(f'/items/{item_id}/edit', data=dict(
                title=title,
                description=description,
                category=category,
                condition=condition,
                location=location,
                contact=contact,
                image=image
            ), follow_redirects=True)

    def delete(self):
        with flaskr.app.app_context():
            db = flaskr.get_db()
            item = db.execute("SELECT * FROM items").fetchone()
            item_id = item["id"]
            return self.app.post(f'/items/{item_id}/delete', follow_redirects=True)

    def search(self, title):
        return self.app.post('/search', data=dict(title=title), follow_redirects=True)

    # codehelp, helped me with the logic behind the data
    def block_user(self):
        return self.app.get('/blocked_users?blocked_user=admin2', follow_redirects=True)
    
    def unblock_user(self):
        return self.app.get('/unblock_user', query_string={'unblock-form': '2'}, follow_redirects=True)
    
    def logout(self):
        return self.app.post('/logout', follow_redirects=True)

    def test_login_logout(self):
        self.complete_registration('admin', 'admin@iwu.edu', 'default')
        rv = self.login('admin', 'default')
        assert b'Welcome, admin' in rv.data
        rv = self.logout()
        assert b'Logged out.' in rv.data

    def test_create_item(self):
        self.complete_registration('admin', 'admin@iwu.edu', 'default')
        self.login('admin', 'default')
        rv = self.create_item('desk', 'a nick desk', 'Other',
                              'Good', 'Magil', '123@iwu.edu', None)
        assert b'Item posted!' in rv.data

        with flaskr.app.app_context():
            db = flaskr.get_db()
            items = db.execute("SELECT * FROM items").fetchall()
            assert len(items) == 1

    def test_edit_item(self):
        self.complete_registration('admin', 'admin@iwu.edu', 'default')
        self.login('admin', 'default')
        self.create_item('desk', 'a nick desk', 'Other',
                         'Good', 'Magil', '123@iwu.edu', None)

        rv = self.edit('Lamp', 'desk lamp', 'Other',
                         'Good', 'Magil', '123@iwu.edu', None)
        assert b"Item updated!" in rv.data

        with flaskr.app.app_context():
            db = flaskr.get_db()
            item = db.execute("SELECT * FROM items").fetchone()
            assert item["title"] == "Lamp"

    def test_delete_item(self):
        self.complete_registration('admin', 'admin@iwu.edu', 'default')
        self.login('admin', 'default')
        self.create_item('desk', 'a nick desk', 'Other',
                         'Good', 'Magil', '123@iwu.edu', None)
        rv = self.delete()
        assert b"Item deleted successfully." in rv.data

    def test_search(self):
        self.complete_registration('admin', 'admin@iwu.edu', 'default')
        self.login('admin', 'default')
        self.create_item('desk', 'a nick desk', 'Other',
                         'Good', 'Magil', '123@iwu.edu', None)
        self.create_item('lamp', 'lamp desk', 'Other',
                         'Good', 'Magil', '123@iwu.edu', None)
        rv = self.search('desk')
        assert b"desk" in rv.data
        assert b"lamp" not in rv.data

    def test_block_user(self):
        self.complete_registration('admin', 'admin@iwu.edu', 'default')
        self.complete_registration('admin2', 'admin2@iwu.edu', 'default')

        self.login('admin2', 'default')
        self.create_item('desk', 'a nick desk', 'Other',
                         'Good', 'Magil', '123@iwu.edu', None)
        self.logout()

        self.login('admin', 'default')

        self.block_user()

        rv = self.search('desk')
        assert b'desk' not in rv.data
    
    def test_unblock_user(self):
        self.complete_registration('admin', 'admin@iwu.edu', 'default')
        self.complete_registration('admin2', 'admin2@iwu.edu', 'default')

        self.login('admin2', 'default')
        self.create_item('desk', 'a nick desk', 'Other',
                         'Good', 'Magil', '123@iwu.edu', None)
        self.logout()

        self.login('admin', 'default')

        self.block_user()

        rv = self.search('desk')
        assert b'desk' not in rv.data

        self.unblock_user()
        assert b'desk' in rv.data

if __name__ == '__main__':
    unittest.main()