from flask import Flask
import os
import sqlite3
import uuid  # to keep filename unique
from flask import Flask, g, render_template, request, redirect, url_for, flash, session, send_from_directory

from werkzeug.utils import secure_filename  # helper that sanitizes untrusted filenames


# app config
app = Flask(__name__)  # creates the flask app object

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # gets the absolute path to the folder

app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),
    DATABASE=os.path.join(BASE_DIR, "database.db"),  # absolute filesystem path to the SQLite database file
    UPLOAD_FOLDER=os.path.join(BASE_DIR, "static", "uploads"),  # path where uploaded files will be saved
    MAX_CONTENT_LENGTH=2 * 1024 * 1024,  # limiting the size of the uploading file
    ALLOWED_EXTENSIONS={"png", "jpg", "jpeg", "gif", "webp"},  # allowed img extensions
)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# db helpers
def get_db():
    if "db" not in g:
        rv = sqlite3.connect(app.config["DATABASE"])
        rv.row_factory = sqlite3.Row
        g.db = rv
    return g.db


@app.teardown_appcontext  # runs at the end of the application context
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()  # closes the sqlite connection


def init_db():
    db = get_db()
    with open(os.path.join(BASE_DIR, "schema.sql"), "r", encoding="utf-8") as f:
        db.executescript(f.read())
    db.commit()


@app.cli.command("init-db")
def init_db_command():
    """Creates the database table."""
    init_db()
    print("Initialized the database.")


def login_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.route("/register", methods=["GET", "POST"])
def register():




if __name__ == "__main__":
    app.run(debug=True)