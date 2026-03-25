import logging
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from db.sqlite_auth import get_user_by_username
from validators import validate_username, validate_password

auth_bp = Blueprint("auth", __name__)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


@auth_bp.route("/")
def index():
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        valid_username, username_message = validate_username(username)
        valid_password, password_message = validate_password(password)

        if not valid_username:
            flash(username_message)
            logging.warning("Login validation failed for username input.")
            return render_template("login.html")

        if not valid_password:
            flash(password_message)
            logging.warning("Login validation failed for password input.")
            return render_template("login.html")

        user = get_user_by_username(current_app.config["AUTH_DB_PATH"], username)

        if user is None:
            flash("Invalid username or password.")
            logging.warning("Failed login attempt for unknown username: %s", username)
            return render_template("login.html")

        if user["active"] != 1:
            flash("This account is inactive.")
            logging.warning("Inactive account login attempt: %s", username)
            return render_template("login.html")

        if not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.")
            logging.warning("Failed login attempt for username: %s", username)
            return render_template("login.html")

        session.clear()
        session.permanent = True
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        session["linked_patient_id"] = user["linked_patient_id"]

        logging.info("Successful login for username: %s with role: %s", username, user["role"])

        if user["role"] == "patient":
            return redirect(url_for("patient.dashboard"))
        if user["role"] == "clinician":
            return redirect(url_for("clinician.dashboard"))
        if user["role"] == "admin":
            return redirect(url_for("admin.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    username = session.get("username", "unknown")
    session.clear()
    logging.info("User logged out: %s", username)
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))