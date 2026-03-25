from flask import Blueprint, render_template
from auth_helpers import login_required, role_required

patient_bp = Blueprint("patient", __name__, url_prefix="/patient")


@patient_bp.route("/dashboard")
@login_required
@role_required("patient")
def dashboard():
    return render_template("patient_dashboard.html")