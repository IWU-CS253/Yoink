import os
import sqlite3
import yagmail
from functools import wraps
from datetime import datetime, timedelta
from flask import g, request, redirect, url_for, flash, session
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Client for sending emails
yag = yagmail.SMTP(os.environ.get("EMAIL_USERNAME", "digreddit7@gmail.com"), os.environ.get("EMAIL_PASSWORD", "urgz cynk hnoi uhov"))

def get_db():
    if "db" not in g:
        from flask import current_app
        rv = sqlite3.connect(current_app.config["DATABASE"])
        rv.row_factory = sqlite3.Row
        g.db = rv
    return g.db

# Decorator for allowing only a certain amount of requests per interval per ip address
def rate_limit_by_user(max_calls: int, interval: int):
    request_history: dict[str, list[datetime]] = {}
    def inner_rate_limit_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.method == "GET":
                return f(*args, **kwargs)

            user_id = session["user_id"]

            if not user_id:
                return "Abort.", 429

            now = datetime.now()
            cutoff_time = now - timedelta(seconds=interval)

            calls = request_history.get(user_id, [])
            new_calls = []

            for call_timestamp in calls:
                if call_timestamp >= cutoff_time:
                    new_calls.append(call_timestamp)

            if len(new_calls) >= max_calls:
                flash("Too many requests. Wait a few seconds then try again.")
                return redirect(url_for("items.index"))

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

# Login required decorator
def login_required(f):
    @wraps(f)
    def login_required_decorator(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return login_required_decorator

# Authorization required decorator
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

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

def save_image(file_storage, upload_folder: str, allowed_extensions: set):
    if not file_storage or not file_storage.filename:
        return None

    filename = os.path.basename(file_storage.filename)

    if "." not in filename or filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
        raise ValueError("File type not allowed.")

    dest_path = os.path.join(upload_folder, filename)
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