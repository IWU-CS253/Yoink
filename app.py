import os
import sqlite3
from flask import Flask, g
from utils import BASE_DIR, get_db

app = Flask(__name__)  # creates the flask app object

app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),  # signs sessions
    DATABASE=os.path.join(BASE_DIR, "database.db"),  # absolute filesystem path to the SQLite database file
    UPLOAD_FOLDER=os.path.join(BASE_DIR, "static", "uploads"),  # path where uploaded files will be saved
    MAX_CONTENT_LENGTH=7 * 1024 * 1024,  # limiting the size of the uploading file (7mb)
    ALLOWED_EXTENSIONS={"png", "jpg", "jpeg", "gif", "webp", "heic"},  # allowed img extensions (need to add heic file as mostly people use iphone)
)

@app.teardown_appcontext  # runs at the end of the application context
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()  # closes the sqlite connection

# initializes the DB from schema
def init_db():
    db = get_db()
    with open(os.path.join(BASE_DIR, "schema.sql"), "r", encoding="utf-8") as f:
        db.executescript(f.read())
    db.commit()

@app.cli.command("initdb")
def init_db_command():
    """Creates the database table."""
    init_db()
    print("Initialized the database.")

# Import blueprints
from routes.auth import auth_bp
from routes.items import items_bp
from routes.users import users_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)
app.register_blueprint(users_bp)

# checks the existence of the upload directory
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

if __name__ == "__main__":
    app.run(debug=True)