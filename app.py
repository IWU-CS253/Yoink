import os
import sqlite3
import yagmail
import random
from functools import wraps
from datetime import datetime, timedelta
from flask import Flask, g, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv

app = Flask(__name__)  # creates the flask app object

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # gets the absolute path to the folder

app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),  # signs sessions
    DATABASE=os.path.join(BASE_DIR, "database.db"),  # absolute filesystem path to the SQLite database file
    UPLOAD_FOLDER=os.path.join(BASE_DIR, "static", "uploads"),  # path where uploaded files will be saved
    MAX_CONTENT_LENGTH=7 * 1024 * 1024,  # limiting the size of the uploading file (7mb)
    ALLOWED_EXTENSIONS={"png", "jpg", "jpeg", "gif", "webp", "heic"},  # allowed img extensions (need to add heic file as mostly people use iphone)
)

# checks the existence of the upload directory
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Client for sending emails
yag = yagmail.SMTP(os.environ.get("EMAIL_USERNAME", "digreddit7@gmail.com"), os.environ.get("EMAIL_PASSWORD", "urgz cynk hnoi uhov"))

def get_db():
    if "db" not in g: # one connection per request
        rv = sqlite3.connect(app.config["DATABASE"])
        rv.row_factory = sqlite3.Row
        g.db = rv
    return g.db


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


# Decorator for allowing only a certain amount of requests per interval per ip address
def rate_limit_by_user(max_calls: int, interval: int):

    # Create request history inside the decorator, so every endpoint has its own limits
    request_history: dict[str, list[datetime]] = {}
    def inner_rate_limit_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # Early return for GET requests
            if request.method == "GET":
                return f(*args, **kwargs)

            user_id = session["user_id"]

            if not user_id:
                return "Abort.", 429

            # Find cutoff time first
            now = datetime.now()
            cutoff_time = now - timedelta(seconds=interval)

            # Update calls by eliminating those before the cutoff time
            calls = request_history.get(user_id, [])
            new_calls = []

            for call_timestamp in calls:
                # Allow only those requests where the timestamp is above the cutoff time
                if call_timestamp >= cutoff_time:
                    new_calls.append(call_timestamp)


            if len(new_calls) >= max_calls:
                flash("Too many requests. Wait a few seconds then try again.")
                # Not a big fan of redirecting users to the main page, but it's enough for this project
                return redirect(url_for("items.index"))

            # Add current timestamp to the call history
            new_calls.append(now)
            request_history[user_id] = new_calls

            return f(*args, **kwargs)
        
        return wrapper
    return inner_rate_limit_decorator

# Decorator for allowing only a certain number of requests per interval per identifier (email in our case)
def rate_limit_by_identifier(max_calls: int, interval: int):
    request_history: dict[str, list[datetime]] = {}
    def rate_limit_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # Early return for GET requests
            if request.method == "GET":
                return f(*args, **kwargs)
            
            identifier = request.form.get("email")

            if not identifier:
                return "Abort.", 429
            
            now = datetime.now()
            cutoff_time = now - timedelta(seconds=interval)
            
            calls = request_history.get(identifier, [])
            new_calls = []

            for call_timestamp in calls:
                if call_timestamp > cutoff_time:
                    new_calls.append(call_timestamp)

            if len(new_calls) >= max_calls:
                print("Too many requests for identifier: ", identifier)
                flash("Too many requests.", "warning")
                return redirect(url_for("items.index"))

            new_calls.append(now)
            request_history[identifier] = new_calls

            return f(*args, **kwargs)
        
        return wrapper
    return rate_limit_decorator
# Login required decorator, to avoid non-browser requests from spamming api requests
def login_required(f):
    @wraps(f)
    def login_required_decorator(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)
    return login_required_decorator

# Authorization required decorator, to avoid bad actors from deleting people's posts
def owns_resource(f):
    @wraps(f)
    def owns_resource_decorator(item_id: int):
        db = get_db()
        rows = db.execute("SELECT items.id FROM items WHERE items.owner_id = ? AND items.id = ?", [session["user_id"], item_id])

        if len(list(rows)) == 0:
            flash("Unauthorized (Kyle please stop it 😭).", "warning")
            return redirect(url_for("items.index"))

        return f(item_id)
    return owns_resource_decorator

# Import blueprints
from routes.auth import auth_bp
from routes.items import items_bp
from routes.users import users_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)
app.register_blueprint(users_bp)


# checks that the filename has an extension at the end
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def save_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None

    # keep the original name, but strip any path parts
    filename = os.path.basename(file_storage.filename)

    # simple allow-list check using your existing config
    if "." not in filename or filename.rsplit(".", 1)[1].lower() not in app.config["ALLOWED_EXTENSIONS"]:
        raise ValueError("File type not allowed.")

    dest_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file_storage.save(dest_path)

    return f"uploads/{filename}"


def placeholder_helper(ls):
    """Helper function for creating placeholders if needed."""

    # creating a placeholder dynamically for all the
    # users that the current user has blocked
    question_mark_placeholder = ""
    for i in range(len(ls.split(", "))):
        question_mark_placeholder = question_mark_placeholder + "?"
        question_mark_placeholder = question_mark_placeholder + ", "
    question_mark_placeholder = question_mark_placeholder[:-2]
    return question_mark_placeholder

if __name__ == "__main__":
    app.run(debug=True)


