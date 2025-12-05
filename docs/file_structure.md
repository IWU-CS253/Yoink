# File Structure

This file briefly explains what the file structure looks like for our project (Yoink)

## Root Files
1. **app.py** - main flask application file, registers blueprints and sets up config
2. **utils.py** - helper functions like get_db(), BASE_DIR, and other utilities
3. **schema.sql** - database schema with tables for users, items, blocked_users
4. **database.db** - sqlite database file
5. **requirements.txt** - python dependencies
6. **how_to_run.md** - instructions for running the app
7. **Unittest.py** - unit tests for the application
8. **.env** - environment variables (not in git, and should never be)
9. **.env.example** - example environment file

## routes/
Split route handlers into separate blueprint files 
- read more about flask blueprints here: https://flask.palletsprojects.com/en/stable/blueprints/
1. **auth.py** - authentication routes (login, register, logout, otp)
2. **items.py** - item CRUD operations (create, read, update, delete, search)
3. **users.py** - user profile and management routes

## templates/
HTML templates using flask's default template engine (jinja2)

1. **layout.html** - base template
2. **login.html** - login page
3. **register.html** - registration page
4. **otp_registration.html** - otp setup
5. **items_list.html** - browse all items
6. **items_new.html** - create new item form
7. **items_edit.html** - edit item form
8. **item_detail.html** - single item view
9. **my_items.html** - owned items
10. **user_profile.html** - view user profile
11. **blocked_users_list.html** - list of blocked users

## static/
1. **styles.css** - main stylesheet
2. **uploads/** - user uploaded images stored here
3. **Images/** - static images for the site

## docs/
Project documentation and reports

1. **user_stories.md**
2. **iteration_report_1.md**
3. **iteration_report_2.md**
4. **iteration_report_3.md**
5. **first_week_iteration.md**

## Other

1. **venv/** - virtual environment (not in git, but locally there should always be one)
2. **.github/** - github workflows and config
