from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from auth_helpers import login_required, role_required
from db.sqlite_auth import get_all_users, create_user, toggle_user_active, get_user_by_username
from validators import validate_username, validate_password, validate_role, validate_patient_id

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
@role_required("admin")
def dashboard():
    db_path = current_app.config["AUTH_DB_PATH"]

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "").strip()
        linked_patient_id = request.form.get("linked_patient_id", "").strip()

        valid_username, message = validate_username(username)
        if not valid_username:
            flash(message)
            users = get_all_users(db_path)
            return render_template("admin_dashboard.html", users=users)

        valid_password, message = validate_password(password)
        if not valid_password:
            flash(message)
            users = get_all_users(db_path)
            return render_template("admin_dashboard.html", users=users)

        valid_role_value, message = validate_role(role)
        if not valid_role_value:
            flash(message)
            users = get_all_users(db_path)
            return render_template("admin_dashboard.html", users=users)

        if role == "patient":
            valid_patient, message = validate_patient_id(linked_patient_id)
            if not valid_patient:
                flash("Patient accounts require a valid linked patient ID.")
                users = get_all_users(db_path)
                return render_template("admin_dashboard.html", users=users)
        else:
            linked_patient_id = None

        existing_user = get_user_by_username(db_path, username)
        if existing_user:
            flash("Username already exists.")
            users = get_all_users(db_path)
            return render_template("admin_dashboard.html", users=users)

        create_user(db_path, username, password, role, linked_patient_id)
        flash("User created successfully.")
        return redirect(url_for("admin.dashboard"))

    users = get_all_users(db_path)
    return render_template("admin_dashboard.html", users=users)


@admin_bp.route("/toggle_user/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def toggle_user(user_id):
    toggle_user_active(current_app.config["AUTH_DB_PATH"], user_id)
    flash("User account status updated.")
    return redirect(url_for("admin.dashboard"))