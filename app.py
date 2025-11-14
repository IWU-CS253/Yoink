import os
import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, flash, session

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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not email or not password:
            flash("Username, email, and password are required.", "danger")
            return render_template("register.html")
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password),
            )
            db.commit()
            flash("Registered! You can log in now.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "danger")
    return render_template("register.html") if os.path.exists(
        os.path.join(BASE_DIR, "templates", "register.html")
    ) else render_template("layout.html", content="(Add register.html or use /login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        db = get_db()
        row = db.execute("SELECT id, username, password FROM users WHERE username = ?", (username,)).fetchone()
        if row and row["password"] == password:
            session["user_id"] = row["id"]
            session["username"] = row["username"]
            flash(f"Welcome, {row['username']}", "success")
            return redirect(request.args.get("next") or url_for("list_items"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html") if os.path.exists(
        os.path.join(BASE_DIR, "templates", "login.html")
    ) else render_template("layout.html", content="(Add login.html Use /register to create a user.")


@app.post("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("list_items"))


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


@app.route("/")
def index():
    return redirect(url_for("list_items"))


@app.get("/items")
def list_items():
    db = get_db()
    rows = db.execute("""
    SELECT items.*, users.username
    FROM items
    JOIN users ON users.id = items.owner_id
    ORDER BY created_at DESC, id DESC
    LIMIT 100
    """).fetchall()
    return render_template("items_list.html", items=rows)


@app.get("/items/<int:item_id>")
def item_detail(item_id: int):
    db = get_db()
    row = db.execute("""
    SELECT items.*, users.username, users.email
    FROM items
    JOIN users ON users.id = items.owner_id
    WHERE items.id = ?
    """, (item_id,)).fetchone()
    if not row:
        flash("Item not found.", "warning")
        return redirect(url_for("list_items"))
    return render_template("item_detail.html", item=row)


@app.route("/items/new", methods=["GET", "POST"])
def create_item():
    if "user_id" not in session:
        flash("Please log in to post an item.", "warning")
        return redirect(url_for("login", next=request.url))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip() or None
        condition = request.form.get("condition", "").strip() or None
        location = request.form.get("location", "").strip() or None
        contact = request.form.get("contact", "").strip()
        image = request.files.get("image")

        errors = []
        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not contact:
            errors.append("Contact is required.")

        image_path = None
        try:
            if image and image.filename:
                image_path = save_image(image)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            for e in errors: flash(e, "danger")
            return render_template("items_new.html",
                                   form=request.form,
                                   username=session.get("username"))
        db = get_db()
        db.execute("""
            INSERT INTO items (owner_id, title, description, category, condition, location, contact, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (session["user_id"], title, description, category, condition, location, contact, image_path))
        db.commit()

        flash("Item posted!", "success")
        return redirect(url_for("list_items"))

    return render_template("items_new.html", username=session.get("username"))

@app.route("/user_profile ", methods=["GET", "POST"])
def user_profile():
    user = request.form["profile_username"]

    db = get_db()
    rows = db.execute("""
                      SELECT *
                      FROM items
                        JOIN users ON users.id = items.owner_id
                      ORDER BY created_at DESC, id DESC LIMIT 100
                      """).fetchall()
    return(render_template("user_profile.html", user_name=user))
@app.route("/my-items", methods=["GET"])
def my_items():

    db = get_db()

    items = db.execute("SELECT * FROM items WHERE items.owner_id = ?", [session["user_id"]]).fetchall()

    return render_template("my_items.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)


