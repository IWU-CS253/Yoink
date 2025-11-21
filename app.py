import os
import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)  # creates the flask app object

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


@app.cli.command("init-db")
def init_db_command():
    """Creates the database table."""
    init_db()
    print("Initialized the database.")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()  # fetches the fields and returns "" if missing
        email = request.form.get("email", "").strip()  # strip removes any whitespace
        password = request.form.get("password", "").strip()
        if not username or not email or not password:
            flash("Username, email, and password are required.", "danger")
            return render_template("register.html")
        db = get_db()  # get database connection
        try:
            db.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password),
            )
            db.commit()  # makes the changes permanent
            flash("Registered! You can log in now.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:  # shows error when there's a duplicate value
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
    return redirect(url_for("list_items"))  # only shows the listed items on the app


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


@app.route("/")
def index():
    return redirect(url_for("list_items"))


@app.get("/items")
def list_items():

    # redirects the user to the login page if logged out
    if "user_id" not in session:
        return redirect(url_for("login"))



    # otherwise we get all of the currently blocked users, split them into a list
    # and add the current users id to that list
    db = get_db()
    current_blocked_users = db.execute("select blocked_user_ids from users where id = ?", [session["user_id"]]).fetchone()

    # if the user doesnt have any users blocked we just
    # display all the post not including the user's posts
    if current_blocked_users[0] == None:
        rows = db.execute("SELECT items.*, users.username FROM items JOIN users ON users.id = items.owner_id WHERE owner_id  != ? ORDER BY created_at DESC, id DESC LIMIT 100", [session["user_id"]])
        return render_template("items_list.html", items=rows)

    # creating a list of values by splitting the
    # current blocked user. Then we add the current users
    # id to the end since that will be used to restrict users
    # from seeing their own items on the list_items page
    values = current_blocked_users[0].split(", ")
    values.append(str(session["user_id"]))

    # creating a placeholder dynamically for all the
    # users that the current user has blocked
    question_mark_placeholder = ""
    for i in range(len(current_blocked_users[0].split(", "))):
        question_mark_placeholder = question_mark_placeholder + "?"
        question_mark_placeholder = question_mark_placeholder + ", "
    question_mark_placeholder = question_mark_placeholder[:-2]

    #  creating a query string to keep all data secure and passing
    # our values into the query
    query = f"SELECT items.*, users.username FROM items JOIN users ON users.id = items.owner_id WHERE owner_id  not in ({question_mark_placeholder}) and owner_id  != ? ORDER BY created_at DESC, id DESC LIMIT 100"
    rows = db.execute(query, values).fetchall()
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


@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id: int):
    db = get_db()
    item = db.execute("SELECT * FROM items WHERE id = ?", (item_id, )).fetchone()

    if not item:
        flash("Item not found.", "warning")
        return redirect(url_for("my_items"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        condition = request.form.get("condition", "").strip()
        location = request.form.get("location", "").strip()
        contact = request.form.get("contact", "").strip()
        image = request.files.get("image")

        errors = []
        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not contact:
            errors.append("Contact is required.")

        image_path = item["image_path"]
        try:
            if image and image.filename:
                image_path = save_image(image)
        except ValueError as e:
            errors.append(str(e))

        if errors:
            for e in errors:
                flash(e, "danger")
                return render_template("items_edit.html", item=item, form=request.form)

        db.execute("""
        UPDATE items 
        SET title = ?, description = ?, category = ?, condition = ?, location = ?, 
        contact = ?, image_path = ?
        WHERE id = ?
        """, (title, description, category, condition, location, contact, image_path, item_id))
        db.commit()

        flash("Item updated!", "success")
        return redirect(url_for("my_items"))

    return render_template("items_edit.html", item=item)


@app.route("/items/<int:item_id>/delete", methods=['POST'])
def delete_item(item_id: int):
    db = get_db()
    item = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()

    flash("Item deleted successfully.", "success")
    return redirect(url_for("my_items"))


@app.route("/user_profile ", methods=["GET", "POST"])
def user_profile():
    """Displays a users profile so users can interact with one another"""
    user_name = request.form["profile_username"]

    db = get_db()
    user_id = db.execute("SELECT id FROM users WHERE username = ?", [user_name]).fetchall()
    items = db.execute(" SELECT * FROM items  where owner_id = ?", [user_id[0][0]]).fetchall()

    return(render_template("user_profile.html", user_name=user_name, items=items))
@app.route("/my-items", methods=["GET"])
def my_items():

    db = get_db()

    items = db.execute("SELECT * FROM items WHERE items.owner_id = ?", [session["user_id"]]).fetchall()

    return render_template("my_items.html", items=items)

@app.route("/search", methods=["POST"])
def search():
    db = get_db()

    if request.form['title'] == '':
        sorted_items = db.execute('SELECT * FROM items ORDER BY created_at DESC')
    else:
        sorted_items = db.execute('SELECT * FROM items WHERE LOWER(items.title) LIKE LOWER(?) ORDER BY created_at DESC', [request.form['title']]).fetchall()

    return render_template("items_list.html", items=sorted_items)
@app.route("/blocked_users", methods=[ "GET"] )
def blocked_users():
    """Allows users to block other users."""

    # accessing the database to get all the
    # users blocked by the current user
    db = get_db()
    current_blocked_users = db.execute("select blocked_user_ids from users where id = ?", [session["user_id"]]).fetchone()

    # getting the current user's id and the username of the blocked user
    # submitted via block button. Then using the blocked user's username
    # to query the database for their id.
    current_user_id = session["user_id"]
    blocked_user = request.args["blocked_user"]
    blocked_user_id = db.execute("SELECT id FROM users WHERE username = ?", [blocked_user]).fetchall()[0][0]

    # if the user hasn't blocked anyone yet, we update their blocked_users_ids
    # to that user and redirect them to the homepage or list items page.
    if current_blocked_users[0] == None and blocked_user_id != current_user_id:
        db.execute("update users set blocked_user_ids = ? where id=?", [str(blocked_user_id), session["user_id"]])
        db.commit()
        return redirect(url_for('list_items'))

    # if the user has already blocked one or more users, we update the
    # blocked_user_ids to contain the newly blocked user
    elif str(blocked_user_id) not in current_blocked_users[0] and  blocked_user_id != current_user_id:
        placeholder = current_blocked_users[0] + ', ' + str(blocked_user_id)
        db.execute("update users set blocked_user_ids = ? where id=?", [placeholder, session["user_id"]])
        db.commit()
        flash(f"{blocked_user} is now blocked!", "danger")
        return redirect(url_for('list_items'))

    # should be good to remove this when i fix the homepage
    return redirect(url_for('list_items'))

if __name__ == "__main__":
    app.run(debug=True)


