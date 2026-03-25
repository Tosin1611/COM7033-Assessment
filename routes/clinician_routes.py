import logging
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from auth_helpers import login_required, role_required
from db.mongo_records import (
    search_patient_records,
    get_patient_record,
    add_consultation_note,
    add_prescription,
    add_appointment,
    update_patient_basic_details
)
from validators import (
    validate_patient_id,
    validate_name,
    validate_age,
    validate_text_field,
    validate_date
)

clinician_bp = Blueprint("clinician", __name__, url_prefix="/clinician")


@clinician_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
@role_required("clinician")
def dashboard():
    results = []

    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip()
        full_name = request.form.get("full_name", "").strip()

        if patient_id:
            valid_patient_id, message = validate_patient_id(patient_id)
            if not valid_patient_id:
                flash(message)
                return render_template("clinician_dashboard.html", results=[])

        results = search_patient_records(
            patient_id=patient_id if patient_id else None,
            full_name=full_name if full_name else None
        )

    return render_template("clinician_dashboard.html", results=results)


@clinician_bp.route("/patient/<patient_id>")
@login_required
@role_required("clinician")
def view_patient(patient_id):
    record = get_patient_record(patient_id)
    if not record:
        flash("Patient record not found.")
        return redirect(url_for("clinician.dashboard"))

    return render_template("clinician_patient.html", record=record)


@clinician_bp.route("/patient/<patient_id>/update", methods=["POST"])
@login_required
@role_required("clinician")
def update_patient(patient_id):
    full_name = request.form.get("full_name", "").strip()
    age = request.form.get("age", "").strip()
    blood_pressure = request.form.get("blood_pressure", "").strip()
    cholesterol = request.form.get("cholesterol", "").strip()
    resting_ecg = request.form.get("resting_ecg", "").strip()
    medical_history = request.form.get("medical_history", "").strip()

    valid_name, message = validate_name(full_name)
    if not valid_name:
        flash(message)
        return redirect(url_for("clinician.view_patient", patient_id=patient_id))

    valid_age, message = validate_age(age)
    if not valid_age:
        flash(message)
        return redirect(url_for("clinician.view_patient", patient_id=patient_id))

    for field_value, field_name in [
        (blood_pressure, "Blood pressure"),
        (cholesterol, "Cholesterol"),
        (resting_ecg, "Resting ECG"),
        (medical_history, "Medical history")
    ]:
        valid, message = validate_text_field(field_value, field_name, 1, 200)
        if not valid:
            flash(message)
            return redirect(url_for("clinician.view_patient", patient_id=patient_id))

    updates = {
        "full_name": full_name,
        "age": int(age),
        "blood_pressure": blood_pressure,
        "cholesterol": cholesterol,
        "resting_ecg": resting_ecg,
        "medical_history": medical_history
    }

    update_patient_basic_details(patient_id, updates)
    logging.info("Clinician %s updated patient record %s", session.get("username"), patient_id)
    flash("Patient details updated successfully.")
    return redirect(url_for("clinician.view_patient", patient_id=patient_id))


@clinician_bp.route("/patient/<patient_id>/add_note", methods=["POST"])
@login_required
@role_required("clinician")
def add_note(patient_id):
    note = request.form.get("note", "").strip()
    date = request.form.get("date", "").strip()

    valid_note, message = validate_text_field(note, "Consultation note", 3, 500)
    if not valid_note:
        flash(message)
        return redirect(url_for("clinician.view_patient", patient_id=patient_id))

    valid_date_value, message = validate_date(date)
    if not valid_date_value:
        flash(message)
        return redirect(url_for("clinician.view_patient", patient_id=patient_id))

    add_consultation_note(patient_id, session.get("username"), note, date)
    flash("Consultation note added successfully.")
    return redirect(url_for("clinician.view_patient", patient_id=patient_id))


@clinician_bp.route("/patient/<patient_id>/add_prescription", methods=["POST"])
@login_required
@role_required("clinician")
def add_new_prescription(patient_id):
    drug = request.form.get("drug", "").strip()
    dosage = request.form.get("dosage", "").strip()
    date = request.form.get("date", "").strip()

    for field_value, field_name in [
        (drug, "Drug"),
        (dosage, "Dosage")
    ]:
        valid, message = validate_text_field(field_value, field_name, 2, 100)
        if not valid:
            flash(message)
            return redirect(url_for("clinician.view_patient", patient_id=patient_id))

    valid_date_value, message = validate_date(date)
    if not valid_date_value:
        flash(message)
        return redirect(url_for("clinician.view_patient", patient_id=patient_id))

    add_prescription(patient_id, drug, dosage, date)
    flash("Prescription added successfully.")
    return redirect(url_for("clinician.view_patient", patient_id=patient_id))


@clinician_bp.route("/patient/<patient_id>/add_appointment", methods=["POST"])
@login_required
@role_required("clinician")
def add_new_appointment(patient_id):
    date = request.form.get("date", "").strip()
    details = request.form.get("details", "").strip()

    valid_date_value, message = validate_date(date)
    if not valid_date_value:
        flash(message)
        return redirect(url_for("clinician.view_patient", patient_id=patient_id))

    valid_details, message = validate_text_field(details, "Appointment details", 3, 200)
    if not valid_details:
        flash(message)
        return redirect(url_for("clinician.view_patient", patient_id=patient_id))

    add_appointment(patient_id, date, details)
    flash("Appointment added successfully.")
    return redirect(url_for("clinician.view_patient", patient_id=patient_id))