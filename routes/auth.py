import os
import sqlite3
import random
import string
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils import get_db, rate_limit_by_identifier, yag, BASE_DIR
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/send-otp', methods=["POST"])
def send_otp():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    otp = request.form.get("otp", "").strip()

    # Someone could get the right otp code, but create an account with a non @iwu.edu domain, by hitting the
    # endpoint directly
    if not str(email).endswith("@iwu.edu"):
        flash("Only IWU students allowed.", 'danger')
        return render_template("register.html")

    db = get_db()  # get database connection

    otp_match = db.execute("SELECT * FROM otp WHERE email = ? AND code = ?", [email, otp]).fetchone()

    if otp_match is None:
        flash("Wrong OTP code.", "danger")
        return render_template("otp_registration.html", email=email, username=username, password=password)

    otp_match_dict = dict(otp_match)

    # Technically not needed, but nice to have.
    if not otp in otp_match_dict.values():
        flash("Wrong OTP code.")
        return render_template("otp_registration.html", email=email, username=username, password=password)

    # Could technically use id, but email and code works fine too.
    db.execute("DELETE FROM otp WHERE email = ? AND code = ?", [email, otp])
    db.commit()

    # Generate password hash, which will be stored in the database
    hashed_password = generate_password_hash(password)

    # Only if all checks go through, register the user
    try:
        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password),
        )
        db.commit()  # makes the changes permanent
        flash("Registered! You can log in now.", "success")
        return redirect(url_for("auth.login"))
    except sqlite3.IntegrityError:  # shows error when there's a duplicate value
        flash("Username or email already exists.", "danger")
        return redirect(url_for("auth.register"))

@auth_bp.route("/register", methods=["GET", "POST"])
@rate_limit_by_identifier(10, 300)
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()  # fetches the fields and returns "" if missing
        email = request.form.get("email", "").strip()  # strip removes any whitespace
        password = request.form.get("password", "").strip()

        if not str(email).endswith("@iwu.edu"):
            flash("Only IWU students allowed.", 'danger')
            return render_template("register.html")

        if not username or not email or not password:
            flash("Username, email, and password are required.", "danger")
            return render_template("register.html")

        # Source - https://stackoverflow.com/a/2257449
        otp_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

        db = get_db()

        db.execute("INSERT INTO otp (code, email) VALUES (?, ?)", [otp_code, email])
        db.commit()

        yag.send(email, "Yoink: Requested OTP Code", f"Your OTP code is: {otp_code}")

        return render_template("otp_registration.html", username=username, email=email, password=password)

    return render_template("register.html") if os.path.exists(
        os.path.join(BASE_DIR, "templates", "register.html")
    ) else render_template("layout.html", content="(Add register.html or use /login")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        db = get_db()

        row = db.execute("SELECT id, username, password FROM users WHERE username = ?", (username,)).fetchone()

        # Check that the hashes are the same to authenticate the user
        if row and check_password_hash(row["password"], password):
            session["user_id"] = row["id"]
            session["username"] = row["username"]
            flash(f"Welcome, {row['username']}", "success")
            return redirect(request.args.get("next") or url_for("items.list_items"))
        
        flash("Invalid username or password.", "danger")
    return render_template("login.html") if os.path.exists(
        os.path.join(BASE_DIR, "templates", "login.html")
    ) else render_template("layout.html", content="(Add login.html Use /register to create a user.")


@auth_bp.post("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("items.list_items"))  # only shows the listed items on the app
