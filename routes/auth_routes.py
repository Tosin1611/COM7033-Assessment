import logging
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from db.sqlite_auth import get_user_by_username

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

        user = get_user_by_username(current_app.config["AUTH_DB_PATH"], username)

        if user is None:
            flash("Invalid username or password.")
            return render_template("login.html")

        if user["active"] != 1:
            flash("This account is inactive.")
            return render_template("login.html")

        if not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        session["linked_patient_id"] = user["linked_patient_id"]

        if user["role"] == "patient":
            return redirect(url_for("patient.dashboard"))
        if user["role"] == "clinician":
            return redirect(url_for("clinician.dashboard"))
        if user["role"] == "admin":
            return redirect(url_for("admin.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))