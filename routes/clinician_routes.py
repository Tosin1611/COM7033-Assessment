from flask import Blueprint, render_template

clinician_bp = Blueprint("clinician", __name__, url_prefix="/clinician")


@clinician_bp.route("/dashboard")
def dashboard():
    return render_template("clinician_dashboard.html")