from flask import Blueprint, render_template
from auth_helpers import login_required, role_required

clinician_bp = Blueprint("clinician", __name__, url_prefix="/clinician")


@clinician_bp.route("/dashboard")
@login_required
@role_required("clinician")
def dashboard():
    return render_template("clinician_dashboard.html")