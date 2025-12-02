from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import get_db, login_required, rate_limit_by_user, owns_resource, save_image, placeholder_helper

items_bp = Blueprint('items', __name__)

@items_bp.route("/")
def index():
    return redirect(url_for("items.list_items"))


@items_bp.get("/items")
@login_required
def list_items():
    """Lists all the items in the database"""
    db = get_db()

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
    question_mark_placeholder = placeholder_helper(current_blocked_users[0])

    #  creating a query string to keep all data secure and passing
    # our values into the query
    query = f"SELECT items.*, users.username FROM items JOIN users ON users.id = items.owner_id WHERE owner_id  not in ({question_mark_placeholder}) and owner_id  != ? ORDER BY created_at DESC, id DESC LIMIT 100"
    rows = db.execute(query, values).fetchall()
    return render_template("items_list.html", items=rows)


@items_bp.get("/items/<int:item_id>")
@login_required
def item_detail(item_id: int):
    """Returns the item details from database"""
    db = get_db()
    row = db.execute("""
    SELECT items.*, users.username, users.email
    FROM items
    JOIN users ON users.id = items.owner_id
    WHERE items.id = ?
    """, (item_id,)).fetchone()
    if not row:
        flash("Item not found.", "warning")
        return redirect(url_for("items.list_items"))
    return render_template("item_detail.html", item=row)


@items_bp.route("/items/new", methods=["GET", "POST"])
@rate_limit_by_user(30, 60 * 60 * 24)
@login_required
def create_item():
    """Adds a post to the website"""

    # takes away the whitespace, and adds all the information to the database
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip() or None
        condition = request.form.get("condition", "").strip() or None
        location = request.form.get("location", "").strip() or None
        contact = request.form.get("contact", "").strip()
        image = request.files.get("image")

        # checks to make sure the user puts in the required data
        errors = []
        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not contact:
            errors.append("Contact is required.")

        image_path = None
        # uploads the image, if image was provided
        try:
            if image and image.filename:
                image_path = save_image(image)
        except ValueError as e:
            errors.append(str(e))

        # if there are any errors, it'll flash red what the error is to the user
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

        # if no errors, the post will be added to the items_list page
        flash("Item posted!", "success")
        return redirect(url_for("items.list_items"))

    return render_template("items_new.html", username=session.get("username"))


@items_bp.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
@rate_limit_by_user(3, 60)
@login_required
@owns_resource
def edit_item(item_id: int):
    """Allows the user to only edit in their own posts"""
    db = get_db()
    item = db.execute("SELECT * FROM items WHERE id = ?", (item_id, )).fetchone()

    # returns error if the item isn't found
    if not item:
        flash("Item not found.", "warning")
        return redirect(url_for("users.my_items"))

    # takes the information from the database
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        condition = request.form.get("condition", "").strip()
        location = request.form.get("location", "").strip()
        contact = request.form.get("contact", "").strip()
        image = request.files.get("image")

        # checks to make sure the user puts in the required data
        errors = []
        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not contact:
            errors.append("Contact is required.")

        # uploads the image, if image was provided
        image_path = item["image_path"]
        try:
            if image and image.filename:
                image_path = save_image(image)
        except ValueError as e:
            errors.append(str(e))

        # if there are any errors, it'll flash red what the error is to the user
        if errors:
            for e in errors:
                flash(e, "danger")
                return render_template("items_edit.html", item=item, form=request.form)

        # updates the database with the edited information
        db.execute("""
        UPDATE items
        SET title = ?, description = ?, category = ?, condition = ?, location = ?,
        contact = ?, image_path = ?
        WHERE id = ?
        """, (title, description, category, condition, location, contact, image_path, item_id))
        db.commit()

        # lets the user know it was updated
        flash("Item updated!", "success")
        return redirect(url_for("users.my_items"))

    return render_template("items_edit.html", item=item)


@items_bp.route("/items/<int:item_id>/delete", methods=['POST'])
@login_required
@owns_resource
def delete_item(item_id: int):
    """Takes the id of the post, then deletes that post"""
    db = get_db()
    # Looks for the item they want to delete
    item = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    # deletes that item
    db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()

    flash("Item deleted successfully.", "success")
    return redirect(url_for("users.my_items"))


@items_bp.route("/search", methods=["POST"])
def search():
    """Searches for specific items"""
    db = get_db()
    search_term = f"%{request.form['title']}%"
    current_blocked_users = db.execute("select blocked_user_ids from users where id = ?",[session["user_id"]]).fetchone()

    # base case: where the user wants to go back to every post
    if request.form['title'] == '':
        sorted_items = db.execute(f'SELECT * FROM items INNER JOIN users ON items.owner_id = users.id Where owner_id not in () ORDER BY created_at DESC')
    else:
        # if not empty, it will show the item based on the characters they use for the search
        sorted_items = db.execute('SELECT * FROM items INNER JOIN users ON items.owner_id = users.id WHERE LOWER(items.title) LIKE LOWER(?) ORDER BY items.created_at DESC', [search_term]).fetchall()

    return render_template("items_list.html", items=sorted_items)
