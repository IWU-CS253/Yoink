from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.dialects.sqlite.base import SQLiteExecutionContext

from utils import get_db, login_required, placeholder_helper

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
    current_blocked_users = db.execute("select blocked_user_ids from users where id = ?",
                                       [session["user_id"]]).fetchone()

    # getting the current user's id and the username of the blocked user
    # submitted via block button. Then using the blocked user's username
    # to query the database for their id. Then using the id to get the other user's
    # blocked_by list so it can be updated
    current_user_id = session["user_id"]
    blocked_user = request.args["blocked_user"]
    blocked_user_id = db.execute("SELECT id FROM users WHERE username = ?", [blocked_user]).fetchall()[0][0]
    blocked_by = db.execute("select blocked_by from users where id = ?",
                            [blocked_user_id]).fetchone()

    # if the user hasn't blocked anyone yet, we update their blocked_users_ids
    # to that user and redirect them to the homepage or list items page.
    if current_blocked_users[0] == None and blocked_user_id != current_user_id:
        db.execute("update users set blocked_user_ids = ? where id=?", [str(blocked_user_id), session["user_id"]])

        # before redirecting the user, we have to check if the other user's
        # blocked_by list and ensure that the current user's id is added to the
        # other user's blocked by column
        if (blocked_by == None or blocked_by[0] == None):
            db.execute("update users set blocked_by = ? where id=?", [session["user_id"], str(blocked_user_id)])
        elif str(session["user_id"]) not in blocked_by[0]:
            placeholder2 = blocked_by[0] + ', ' + str(session["user_id"])
            db.execute("update users set blocked_by = ? where id=?", [placeholder2, blocked_user_id])

        # commit changes and redirect
        db.commit()
        return redirect(url_for('items.list_items'))

    # if the user has already blocked one or more users, we update the
    # blocked_user_ids to contain the newly blocked user
    elif str(blocked_user_id) not in current_blocked_users[0] and  blocked_user_id != current_user_id:

        # copy and paste of the code from above but for this case.
        if (blocked_by == None or blocked_by[0] == None):
            db.execute("update users set blocked_by = ? where id=?", [session["user_id"], str(blocked_user_id)])
        elif str(session["user_id"]) not in blocked_by[0]:
            placeholder2 = blocked_by[0] + ', ' + str(session["user_id"])
            db.execute("update users set blocked_by = ? where id=?", [placeholder2, blocked_user_id])

        # updating the blocked user ids column for the current user to include
        # the newly blocked user
        placeholder = current_blocked_users[0] + ', ' + str(blocked_user_id)
        db.execute("update users set blocked_user_ids = ? where id=?", [placeholder, session["user_id"]])

        # commiting changes, signaling to the user that they successfully
        # blocked a user, then redirecting to the list_items page
        db.commit()
        flash(f"{blocked_user} is now blocked!", "danger")
        return redirect(url_for('items.list_items'))
    return redirect(url_for('items.list_items'))

@users_bp.route("/blocked_users_list")
@login_required
def blocked_users_list():
    """Lists all the users that the current user has blocked."""

    # getting the currently blocked users
    db = get_db()
    blocked_users = db.execute("Select blocked_user_ids from users where id = ?", [session["user_id"]]).fetchone()

    # if there aren't any blocked users, we just render
    # the template with no blocked_users_list
    if blocked_users[0] == None:
        return (render_template("blocked_users_list.html"))

    # creating a placeholder dynamically for all the
    # users that the current user has blocked
    question_mark_placeholder = placeholder_helper(blocked_users[0])

    # creating a query using those placeholders to get all
    # the blocked users
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

    # when a user is unblocked by the current user, we have to remove the
    # current users id from the block_by column of the blocked user. So we
    # query the db and get the blocked_by list from the unblocked user and
    # remove the current user's id from that list.
    blocked_by = db.execute("Select blocked_by from users where id = ?", [unblocked_user]).fetchone()
    blocked_by = blocked_by[0].split(", ")
    blocked_by.remove(str(session["user_id"]))

    # rebuilding our placeholder with the new list
    # and updating the blocked_by column of the unblocked user
    # to the new list without the current user's id
    placeholder2 = ", ".join(blocked_by)
    db.execute("Update users set blocked_by = ? where id = ?", [placeholder2, unblocked_user])
    db.commit()

    # return the current user to the same page which is the list
    # of the remaining users that are blocked. The user also see
    # a success flash indicating the user that was unblocked
    username= db.execute("Select username from users where id =?", [unblocked_user]).fetchone()[0]
    flash(f"{username} is now unblocked. You can now see their post.", "success")
    return (redirect(url_for('users.blocked_users_list')))
