from flask import Blueprint, session, render_template, flash
from auth_helpers import login_required, role_required
from db.mongo_records import get_patient_record

patient_bp = Blueprint("patient", __name__, url_prefix="/patient")


@patient_bp.route("/dashboard")
@login_required
@role_required("patient")
def dashboard():
    patient_id = session.get("linked_patient_id")
    record = get_patient_record(patient_id)

    if not record:
        flash("No patient record found.")
        return render_template("patient_dashboard.html", record=None)

    return render_template("patient_dashboard.html", record=record)