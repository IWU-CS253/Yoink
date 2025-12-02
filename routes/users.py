from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import get_db, login_required, placeholder_helper

users_bp = Blueprint('users', __name__)

@users_bp.route("/user_profile ", methods=["GET", "POST"])
@login_required
def user_profile():
    """Displays a users profile so users can interact with one another"""
    user_name = request.form["profile_username"]

    db = get_db()
    user_id = db.execute("SELECT id FROM users WHERE username = ?", [user_name]).fetchall()
    items = db.execute(" SELECT * FROM items  where owner_id = ?", [user_id[0][0]]).fetchall()

    return(render_template("user_profile.html", user_name=user_name, items=items))

@users_bp.route("/my-items", methods=["GET"])
@login_required
def my_items():
    """Shows the users only their post"""
    db = get_db()

    items = db.execute("SELECT * FROM items WHERE items.owner_id = ?", [session["user_id"]]).fetchall()

    return render_template("my_items.html", items=items)

@users_bp.route("/blocked_users", methods=["GET"])
@login_required
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
        return redirect(url_for('items.list_items'))

    # if the user has already blocked one or more users, we update the
    # blocked_user_ids to contain the newly blocked user
    elif str(blocked_user_id) not in current_blocked_users[0] and  blocked_user_id != current_user_id:
        placeholder = current_blocked_users[0] + ', ' + str(blocked_user_id)
        db.execute("update users set blocked_user_ids = ? where id=?", [placeholder, session["user_id"]])
        db.commit()
        flash(f"{blocked_user} is now blocked!", "danger")
        return redirect(url_for('items.list_items'))

    # should be good to remove this when i fix the homepage
    return redirect(url_for('items.list_items'))

@users_bp.route("/blocked_users_list")
@login_required
def blocked_users_list():
    """Lists all the users that the current user has blocked."""

    # getting the currently blocked users
    db = get_db()
    blocked_users = db.execute("Select blocked_user_ids from users where id = ?", [session["user_id"]]).fetchone()

    # creating a placeholder dynamically for all the
    # users that the current user has blocked
    question_mark_placeholder = placeholder_helper(blocked_users[0])

    # creating a query using those placeholders to get all
    # of the blocked users
    query = f"Select username, id from users where id in ({question_mark_placeholder})"
    blocked_usernames = db.execute(query, blocked_users[0].split(", ")).fetchall()
    return(render_template("blocked_users_list.html", blocked_users_list= blocked_usernames))

@users_bp.route("/unblock_user")
@login_required
def unblock_user():
    """Allows users to unblock users."""

    # getting the currently blocked users and creating a list
    # from them so we can easily remove the user to be unblocked.
    unblocked_user = request.args["unblock-form"]
    db = get_db()
    blocked_users = db.execute("Select blocked_user_ids from users where id = ?", [session["user_id"]]).fetchone()
    blocked_users = blocked_users[0].split(", ")
    blocked_users.remove(unblocked_user)

    # we then convert the new list into a string joined on
    # commas so w can maintain structure. We then update the current
    # users blocked user list in the database.
    placeholder = ", ".join(blocked_users)
    db.execute("Update users set blocked_user_ids = ? where id = ?", [placeholder, session["user_id"]])
    db.commit()

    # return them to the same page which is the list
    # of users that are currently blocked.
    flash(f"{session['username']} is now unblocked. You can now see their post.", "success")
    return (redirect(url_for('users.blocked_users_list')))
